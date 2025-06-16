from django.shortcuts import render, redirect
from .forms import TestCaseForm, TestSummaryForm
from .models import TestCase, TestSummary

# ============================
# View to Add a New Test Case
# ============================
def add_test_case(request):
    # If the form was submitted (HTTP POST request)
    if request.method == 'POST':
        form = TestCaseForm(request.POST)  # Bind form with submitted data
        if form.is_valid():  # Check if all required fields are valid
            form.save()  # Save form data to the database
            return redirect('view_test_cases')  # Redirect to the page that lists all test cases
    else:
        form = TestCaseForm()  # Create an empty form for user to fill in
    # Render the form template and pass the form context to it
    return render(request, 'reports/add_test_case.html', {'form': form})

# ================================
# View to Display All Test Cases
# ================================
def view_test_cases(request):
    test_cases = TestCase.objects.all()  # Fetch all saved test cases from the database
    return render(request, 'reports/view_test_cases.html', {'test_cases': test_cases})  # Display them in a template

# ============================
# View to Add a Test Summary
# ============================
def add_summary(request):
    # If the form was submitted (HTTP POST request)
    if request.method == 'POST':
        form = TestSummaryForm(request.POST)  # Bind form with submitted data
        if form.is_valid():  # Validate the form data
            form.save()  # Save to database
            return redirect('view_summary')  # Redirect to the page showing all summaries
    else:
        form = TestSummaryForm()  # Create an empty summary form
    # Render the form in a template
    return render(request, 'reports/add_summary.html', {'form': form})

# ===================================
# View to Display All Test Summaries
# ===================================
def view_summary(request):
    summaries = TestSummary.objects.all()  # Retrieve all test summaries from the database
    return render(request, 'reports/view_summary.html', {'summaries': summaries})  # Render the summary list page
