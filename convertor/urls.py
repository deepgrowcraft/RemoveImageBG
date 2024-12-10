from django.urls import path

from .views import (
    ConvertDocxToPdf,
    ConvertPptToPdf,
    ConvertToPdf,
    ConvertXlsxToPdf,
    PdfOcrView,
)

urlpatterns = [
    path(
        "convert/docx-to-pdf/", ConvertDocxToPdf.as_view(), name="convert-docx-to-pdf"
    ),
    path("convert/xlsx-to-pdf/", ConvertXlsxToPdf.as_view(), name="convert-xls-to-pdf"),
    path("convert/ppt-to-pdf/", ConvertPptToPdf.as_view(), name="convert-ppt-to-pdf"),
    path("convert/html-to-pdf/", ConvertToPdf.as_view(), name="convert-html-to-pdf"),
    path("convert/pdf-ocr/", PdfOcrView.as_view(), name="convert-pdf-ocr"),
]
