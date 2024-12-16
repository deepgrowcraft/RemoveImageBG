import logging
import os
import subprocess

import fitz  # PyMuPDF
import pdfkit
import pytesseract
from django.core.files.storage import default_storage
from django.http import FileResponse
from PIL import Image
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.conf import settings

logger = logging.getLogger(__name__)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import ast


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


class ExtractPdfContent(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        # Retrieve the file and extraction preferences
        pdf_file = request.FILES.get("file", None)
        extract_all = request.data.get("extract_all", "false").lower() == "true"
        pages = request.data.get("pages", None)

        if not pdf_file:
            return Response({"error": "No file provided"}, status=400)

        # Parse and validate `pages` only if not extracting all
        if not extract_all:
            try:
                if isinstance(pages, str):
                    # Convert string representation of list to actual list
                    pages = ast.literal_eval(pages)
                if not isinstance(pages, list) or not all(
                    isinstance(page, int) for page in pages
                ):
                    return Response(
                        {"error": "`pages` must be a list of integers."}, status=400
                    )
                pages = [page - 1 for page in pages]  # Convert to 0-based indexing
            except Exception:
                return Response(
                    {
                        "error": "Invalid `pages` format. Provide a valid list of integers."
                    },
                    status=400,
                )

        # Save the uploaded PDF temporarily
        pdf_file_path = default_storage.save(f"temp/{pdf_file.name}", pdf_file)
        pdf_file_full_path = default_storage.path(pdf_file_path)

        try:
            extracted_pages = {}

            # Open the PDF
            with fitz.open(pdf_file_full_path) as pdf_document:
                # Determine which pages to process
                if extract_all:
                    page_numbers = range(pdf_document.page_count)  # All pages
                else:
                    page_numbers = pages

                # Validate page numbers
                if any(
                    page < 0 or page >= pdf_document.page_count for page in page_numbers
                ):
                    return Response(
                        {"error": "One or more page numbers are out of range."},
                        status=400,
                    )

                # Process the specified pages
                for page_number in page_numbers:
                    try:
                        print(f"Processing page: {page_number + 1}")

                        # Render the page as an image
                        page = pdf_document[page_number]
                        pix = page.get_pixmap(
                            dpi=150
                        )  # Adjust DPI for better OCR results
                        img = Image.frombytes(
                            "RGB", [pix.width, pix.height], pix.samples
                        )

                        # Perform OCR on the rendered image
                        ocr_text = pytesseract.image_to_string(img)

                        # Clean up extracted text
                        cleaned_text = clean_extracted_text(ocr_text)

                        # Add to the result dictionary
                        extracted_pages[str(page_number + 1)] = (
                            cleaned_text.strip() or "No text detected."
                        )
                    except Exception as e:
                        print(f"Error processing page {page_number + 1}: {e}")
                        extracted_pages[str(page_number + 1)] = f"Error: {str(e)}"

            return Response({"pages": extracted_pages}, status=200)

        except Exception as e:
            print(f"Unhandled exception: {e}")
            return Response({"error": str(e)}, status=500)

        finally:
            # Cleanup the uploaded file
            if os.path.exists(pdf_file_full_path):
                os.remove(pdf_file_full_path)

def clean_extracted_text(text):
    """
    Clean up OCR extracted text to improve readability.
    """
    # Replace unnecessary newlines and tabs with spaces
    text = text.replace("\n", " ").replace("\t", " ")

    # Remove excessive spaces
    text = " ".join(text.split())

    return text

# class UploadPDFView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#
#     def post(self, request, *args, **kwargs):
#         file = request.data.get("file")
#         if not file or file.content_type != "application/pdf":
#             return Response(
#                 {"error": "Invalid file format. Only PDF files are allowed."},
#                 status=400,
#             )
#
#         # Save the file to a temporary location
#         file_path = os.path.join(settings.MEDIA_ROOT, file.name)
#         with open(file_path, "wb") as f:
#             f.write(file.read())
#
#         # Return the file path to be used later
#         return Response({"file_path": file_path}, status=201)


class UploadPDFView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file = request.data.get("file")
        if not file or file.content_type != "application/pdf":
            return Response(
                {"error": "Invalid file format. Only PDF files are allowed."},
                status=400,
            )

        # Save the file to a temporary location
        file_path = default_storage.save(f"temp/{file.name}", file)
        full_file_path = default_storage.path(file_path)

        try:
            # Return the file path to be used later
            return Response({"file_path": full_file_path}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            # Cleanup the uploaded file
            if os.path.exists(full_file_path):
                os.remove(full_file_path)
