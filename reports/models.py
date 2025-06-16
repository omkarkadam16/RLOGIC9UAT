from django.db import models

class TestCase(models.Model):
    test_id = models.IntegerField()
    description = models.TextField()
    test_data = models.TextField(null=True, blank=True)
    actual_result = models.CharField(max_length=255, blank=True, null=True)
    expected_result = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('Passed', 'Passed'), ('Failed', 'Failed')])
    remark = models.TextField(null=True, blank=True)

    def __str__(self): #The __str__ method is a special method in Python that returns a string representation of an object.
        return f"TestCase {self.test_id} - {self.status}"


class TestSummary(models.Model):
    month = models.CharField(max_length=20)
    module_name = models.CharField(max_length=100)
    passed_tests = models.IntegerField()
    failed_tests = models.IntegerField()
    total_test_cases = models.IntegerField()

    def __str__(self):
        return f"Summary {self.module_name} - {self.month}"

# class OrganizationalTestStatus(models.Model):
#     test_id = models.IntegerField()
#     organizational_hierarchy = models.CharField(max_length=100)
#     status = models.CharField(max_length=50)  # e.g., Done
#     rerun_count = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f"OrgStatus {self.test_id} - {self.status}"