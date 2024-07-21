# calculator/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CalculationHistory
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import CalculationHistory


def home(request):
    history = CalculationHistory.objects.order_by('-created_at')[:10]  # Fetch last 10 calculations
    return render(request, 'calculator/home.html', {'history': history})

def calculate(request):
    if request.method == 'POST':
        expression = request.POST.get('expression')
        try:
            result = eval(expression)
            # Save to history
            CalculationHistory.objects.create(expression=expression, result=str(result))
            return render(request, 'calculator/home.html', {'result': result, 'expression': expression})
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'calculator/home.html', {'error_message': error_message})
    return render(request, 'calculator/home.html')
    # calculator/views.py
# calculator/views.py


def download_history(request):
    history_entries = CalculationHistory.objects.all()

    # Create a buffer for the PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="calculation_history.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Table data
    data = [['Expression', 'Result', 'Date']]
    for entry in history_entries:
        data.append([entry.expression, entry.result, entry.created_at.strftime('%Y-%m-%d %H:%M:%S')])

    # Create a table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Create a table object
    table = Table(data)
    table.setStyle(style)
    elements.append(table)

    # Build PDF document
    doc.build(elements)
    return response
