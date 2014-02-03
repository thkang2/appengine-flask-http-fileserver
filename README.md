## Python Flask Skeleton for Google App Engine

A simple http fileserver that you can upload with POST and download with GET.

based on the [A skeleton for building Python applications on Google App Engine with the Flask micro framework](https://github.com/GoogleCloudPlatform/appengine-python-flask-skeleton).

## How to deploy

1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads).

2. Clone this repo.

3. Install dependencies in the project's lib directory.

   ```
   pip install -r requirements.txt -t lib
   ```

4. Write your application settings to `app.yaml`

5. [Deploy the
   application](https://developers.google.com/appengine/docs/python/tools/uploadinganapp) with

   ```
   appcfg.py -A <your-project-id> --oauth2 update .
   ```

6. POST the files to `<your-app-id>.appspot.com/upload`. The response will be a JSON that contains an array which has urls to serve your uploaded files.

7. See the [sample.html](sample.html) for writing frontends to this fileserver.

## Note

The app uses deprecated [Blobstore Files API](https://developers.google.com/appengine/docs/python/blobstore/blobstorefiles). I had no choice but to use them, because [the method](https://developers.google.com/appengine/docs/python/blobstore/#Python_Uploading_a_blob) mentioned in Python Developer's Guide for Blobstore does not support cross-domain requests.

## Licensing
See [LICENSE](LICENSE)


