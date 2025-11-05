from locust import HttpUser, task, between
import json
import os

# Path to the directory containing test files, relative to this locustfile.py
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')

class WebsiteUser(HttpUser):
    """
    User class that loads real files from the 'test_files' directory
    to run more realistic load tests.
    """
    wait_time = between(1, 5)

    @task(1)
    def convert_file(self):
        """ Simulates uploading a real PNG file for conversion. """
        image_path = os.path.join(TEST_FILES_DIR, 'image.png')
        if not os.path.exists(image_path):
            return

        with open(image_path, 'rb') as f:
            files_to_upload = {
                'file': ('image.png', f.read(), 'image/png')
            }
            form_data = {
                'to': 'jpg'
            }
            self.client.post(
                "/convert",
                files=files_to_upload,
                data=form_data,
                name="/convert"
            )

    @task(1)
    def merge_files(self):
        """ Simulates uploading a real PDF file twice for merging. """
        doc_path = os.path.join(TEST_FILES_DIR, 'document.pdf')
        if not os.path.exists(doc_path):
            return

        with open(doc_path, 'rb') as f1:
            file_content_1 = f1.read()
        
        with open(doc_path, 'rb') as f2:
            file_content_2 = f2.read()

        files_to_upload = [
            ('files', ('doc1.pdf', file_content_1, 'application/pdf')),
            ('files', ('doc2.pdf', file_content_2, 'application/pdf'))
        ]
        
        self.client.post(
            "/merge",
            files=files_to_upload,
            name="/merge"
        )

    @task(1)
    def split_file(self):
        """ Simulates uploading a real PDF file for splitting. """
        doc_path = os.path.join(TEST_FILES_DIR, 'document.pdf')
        if not os.path.exists(doc_path):
            return

        with open(doc_path, 'rb') as f:
            files_to_upload = {
                'file': ('document.pdf', f.read(), 'application/pdf')
            }
            
            # CORRECTED: Using "method" and "interval" as expected by the service
            options_data = {"method": "fixed", "interval": 1}
            form_data = {
                'options': json.dumps(options_data)
            }

            self.client.post(
                "/split",
                files=files_to_upload,
                data=form_data,
                name="/split"
            )