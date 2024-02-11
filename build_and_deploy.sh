#! /bin/bash

export PROJECT_ID=crested-primacy-413823
export REGION=us-east1
export CONNECTION_NAME=crested-primacy-413823:us-central1:publications

gcloud builds submit \
  --tag gcr.io/$PROJECT_ID/publications \
  --project $PROJECT_ID

gcloud run deploy publications \
  --image gcr.io/$PROJECT_ID/publications \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNECTION_NAME \
  --project $PROJECT_ID