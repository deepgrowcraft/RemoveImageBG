import logging
import os
import subprocess

import fitz  # PyMuPDF
import pdfkit
import pytesseract
from django.core.files.storage import default_storage
from django.http import FileResponse
from PIL import Image
from rest_framework.parsers import FormParser, MultiPartParser

logger = logging.getLogger(__name__)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ConvertDocxToPdf(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Get the uploaded DOCX file from the request
        docx_file = request.FILES.get("file", None)

        if not docx_file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the DOCX file temporarily
        docx_file_path = default_storage.save(f"temp/{docx_file.name}", docx_file)

        # Define paths for conversion
        docx_file_full_path = default_storage.path(docx_file_path)
        pdf_file_name = os.path.splitext(docx_file.name)[0] + ".pdf"
        pdf_file_path = os.path.join(
            os.path.dirname(docx_file_full_path), pdf_file_name
        )

        try:
            # Use the full path for libreoffice (soffice) on macOS or Linux
            libreoffice_path = (
                "/Applications/LibreOffice.app/Contents/MacOS/soffice"
                if os.path.exists(
                    "/Applications/LibreOffice.app/Contents/MacOS/soffice"
                )
                else "libreoffice"
            )

            # Run the command to convert DOCX to PDF
            subprocess.run(
                [
                    libreoffice_path,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    docx_file_full_path,
                    "--outdir",
                    os.path.dirname(docx_file_full_path),
                ],
                check=True,
            )

            # Check if the PDF file was created
            if not os.path.exists(pdf_file_path):
                return Response(
                    {"error": "PDF file was not created"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Serve the PDF file as a response
            pdf_file = open(pdf_file_path, "rb")
            response = FileResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{pdf_file_name}"'
            return response

        except subprocess.CalledProcessError as e:
            return Response(
                {"error": "File conversion failed: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up the files
            if os.path.exists(docx_file_full_path):
                os.remove(docx_file_full_path)
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)


class ConvertXlsxToPdf(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Get the uploaded Excel file from the request
        excel_file = request.FILES.get("file", None)

        if not excel_file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the Excel file temporarily
        excel_file_path = default_storage.save(f"temp/{excel_file.name}", excel_file)

        # Define paths for conversion
        excel_file_full_path = default_storage.path(excel_file_path)
        pdf_file_name = os.path.splitext(excel_file.name)[0] + ".pdf"
        pdf_file_path = os.path.join(
            os.path.dirname(excel_file_full_path), pdf_file_name
        )

        try:
            # Use the full path for LibreOffice (soffice) on macOS or Linux
            libreoffice_path = (
                "/Applications/LibreOffice.app/Contents/MacOS/soffice"
                if os.path.exists(
                    "/Applications/LibreOffice.app/Contents/MacOS/soffice"
                )
                else "libreoffice"
            )

            # Run the command to convert Excel to PDF
            subprocess.run(
                [
                    libreoffice_path,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    excel_file_full_path,
                    "--outdir",
                    os.path.dirname(excel_file_full_path),
                ],
                check=True,
            )

            # Check if the PDF file was created
            if not os.path.exists(pdf_file_path):
                return Response(
                    {"error": "PDF file was not created"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Serve the PDF file as a response
            pdf_file = open(pdf_file_path, "rb")
            response = FileResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{pdf_file_name}"'
            return response

        except subprocess.CalledProcessError as e:
            return Response(
                {"error": "File conversion failed: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up the files
            if os.path.exists(excel_file_full_path):
                os.remove(excel_file_full_path)
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)


class ConvertPptToPdf(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Get the uploaded PowerPoint file from the request
        ppt_file = request.FILES.get("file", None)

        if not ppt_file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the PowerPoint file temporarily
        ppt_file_path = default_storage.save(f"temp/{ppt_file.name}", ppt_file)

        # Define paths for conversion
        ppt_file_full_path = default_storage.path(ppt_file_path)
        pdf_file_name = os.path.splitext(ppt_file.name)[0] + ".pdf"
        pdf_file_path = os.path.join(os.path.dirname(ppt_file_full_path), pdf_file_name)

        try:
            # Use the full path for LibreOffice (soffice) on macOS or Linux
            libreoffice_path = (
                "/Applications/LibreOffice.app/Contents/MacOS/soffice"
                if os.path.exists(
                    "/Applications/LibreOffice.app/Contents/MacOS/soffice"
                )
                else "libreoffice"
            )

            # Run the command to convert PowerPoint to PDF
            subprocess.run(
                [
                    libreoffice_path,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    ppt_file_full_path,
                    "--outdir",
                    os.path.dirname(ppt_file_full_path),
                ],
                check=True,
            )

            # Check if the PDF file was created
            if not os.path.exists(pdf_file_path):
                return Response(
                    {"error": "PDF file was not created"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Serve the PDF file as a response
            pdf_file = open(pdf_file_path, "rb")
            response = FileResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{pdf_file_name}"'
            return response

        except subprocess.CalledProcessError as e:
            return Response(
                {"error": "File conversion failed: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up the files
            if os.path.exists(ppt_file_full_path):
                os.remove(ppt_file_full_path)
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)


class ConvertToPdf(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        html_content = request.data.get("html_content", None)

        if not html_content:
            return Response(
                {"error": "No HTML content provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pdf_file_path = default_storage.path("temp/converted_html.pdf")

        try:
            # Use pdfkit to convert HTML to PDF
            pdfkit.from_string(html_content, pdf_file_path)
            pdf_file = open(pdf_file_path, "rb")
            response = FileResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="converted_html.pdf"'
            )
            return response
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            if pdf_file_path and default_storage.exists(pdf_file_path):
                default_storage.delete(pdf_file_path)


class PdfOcrView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        pdf_file = request.FILES.get("file", None)

        if not pdf_file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the PDF file temporarily
        pdf_file_path = default_storage.save(f"temp/{pdf_file.name}", pdf_file)
        pdf_file_full_path = default_storage.path(pdf_file_path)

        try:
            # Initialize OCR text result
            ocr_text = ""

            # Open the PDF with PyMuPDF
            with fitz.open(pdf_file_full_path) as pdf_document:
                for page_number in range(pdf_document.page_count):
                    page = pdf_document[page_number]
                    pix = page.get_pixmap()  # Render page to image
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                    # Perform OCR on the image
                    text = pytesseract.image_to_string(img)
                    ocr_text += f"\n\nPage {page_number + 1}:\n{text}"

            return Response({"ocr_text": ocr_text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        finally:
            # Clean up the file
            if os.path.exists(pdf_file_full_path):
                os.remove(pdf_file_full_path)
