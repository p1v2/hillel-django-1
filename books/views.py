import csv

from django.http import HttpResponse

from books.models import Book

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def books_csv_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Name', 'Pages count', 'Authors', 'Country'])
    for book in Book.objects.all()[:100]:
        writer.writerow([book.name, book.pages_count, book.authors, book.country])
    return response


def books_pdf_export(request):
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Books.pdf')