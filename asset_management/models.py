from django.db import models
from simple_history.models import HistoricalRecords


class Asset(models.Model):
    name = models.CharField(max_length=100 ,blank=True, null=True)
    description = models.TextField()
    acquisition_date = models.DateField()
    initial_value = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null=True)
    status = models.CharField(max_length=50, default='Active')
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


    def __str__(self):
        return self.name
    

class Lifecycle(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,blank=True, null=True)
    stage = models.CharField(max_length=50 ,blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.asset.name} - {self.stage}"
    
    
class Depreciation(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,blank=True, null=True)
    depreciation_date = models.DateField()
    initial_value = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    depreciated_value = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    market_conditions = models.TextField()
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.asset.name

    def calculate_depreciation_rate(self):
        net_depreciated_value = self.depreciated_value + self.maintenance_cost
        return ((self.initial_value - net_depreciated_value) / self.initial_value) * 100
    
class Appreciation(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,blank=True, null=True)
    appreciation_date = models.DateField()
    appreciation_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    appreciation_rate = models.DecimalField(max_digits=5, decimal_places=2 ,default=0.00)   
    market_conditions = models.TextField()
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


    def __str__(self):
        return self.asset.name
    
    def calculate_appreciation_rate(self):
        net_appreciated_value = self.appreciation_value + self.maintenance_cost
        return ((net_appreciated_value - self.asset.initial_value) / self.asset.initial_value) * 100
    
                                           
class Maintenance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE ,blank=True, null=True)
    maintenance_date = models.DateField()
    maintenance_type = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.asset.name} - {self.maintenance_type}"
    
class Risk(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,blank=True, null=True)
    risk_date = models.DateField()
    risk_type = models.CharField(max_length=50)
    mitigation_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


    def __str__(self):
        return f"{self.asset.name} - {self.risk_type}"
    
class Report(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE ,blank=True, null=True)
    report_date = models.DateField()
    report_type = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


    def __str__(self):
        return f"{self.asset.name} - {self.report_type}"
