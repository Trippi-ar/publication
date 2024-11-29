from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from fastapi import UploadFile
from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError

from src.api.publication_ep import router
from src.service.publication_service import PublicationService


client = TestClient(router)


def test_create_publication_ep_successful():
    mock_token = MagicMock()
    mock_token.credentials = "mocked_token"
    mock_request_data = {
        "name": "Test Publication",
        "difficulty": "easy",
        "distance": 10.5,
        "duration": 120,
        "price": 15.0,
        "description": "Test description",
        "tools": "None",
        "type": "public",
        "languages": ["english", "spanish"],
        "max_participants": 20,
        "dates": ["12-02-2025", "13-02-2025"],
        "country": "Test Country",
        "administrative_area_level_1": "Test State",
        "locality": "Test City"
    }
    mock_files = {
        "images": ("test_image.jpg", b"file_content", "image/jpeg")
    }
    mock_uploaded_images = ["uploaded_image_1_url", "uploaded_image_2_url"]

    with patch.object(PublicationService, "create", return_value="mocked_publication_id") as mock_create, \
         patch.object(PublicationService, "upload_image", new_callable=AsyncMock, return_value=mock_uploaded_images) as mock_upload:

        with open(mock_files["images"][0], "wb") as file:
            file.write(mock_files["images"][1])
        files = {"images": (mock_files["images"][0], open(mock_files["images"][0], "rb"), mock_files["images"][2])}

        response = client.post(
            "/api/",
            data=mock_request_data,
            files=files,
            headers={"Authorization": f"Bearer {mock_token.credentials}"}
        )

        assert response.status_code == 201
        assert response.json() == "mocked_publication_id"

        assert mock_upload.await_args.args[0][0].filename == "test_image.jpg"
        assert mock_upload.await_args.args[0][0].content_type == "image/jpeg"


def test_create_publication_ep_fail_upload_image():
    mock_token = MagicMock()
    mock_token.credentials = "mocked_token"
    mock_request_data = {
        "name": "Test Publication",
        "difficulty": "easy",
        "distance": 10.5,
        "duration": 120,
        "price": 15.0,
        "description": "Test description",
        "tools": "None",
        "type": "public",
        "languages": ["english", "spanish"],
        "max_participants": 20,
        "dates": ["12-02-2025", "13-02-2025"],
        "country": "Test Country",
        "administrative_area_level_1": "Test State",
        "locality": "Test City"
    }
    mock_files = {
        "images": ("test_image.jpg", b"file_content", "image/jpeg")
    }
    mock_uploaded_images = ["uploaded_image_1_url", "uploaded_image_2_url"]

    with patch.object(PublicationService, "create", return_value="mocked_publication_id") as mock_create, \
         patch.object(PublicationService, "upload_image", new_callable=AsyncMock, side_effect=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Image upload failed")) as mock_upload:

        with open(mock_files["images"][0], "wb") as file:
            file.write(mock_files["images"][1])
        files = {"images": (mock_files["images"][0], open(mock_files["images"][0], "rb"), mock_files["images"][2])}

        with pytest.raises(HTTPException) as e:
            client.post(
                "/api/",
                data=mock_request_data,
                files=files,
                headers={"Authorization": f"Bearer {mock_token.credentials}"}
            )

        assert e.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert e.value.detail == "Image upload failed"

        mock_upload.assert_awaited_once()


def test_create_publication_ep_invalid_data_distance():
    mock_token = MagicMock()
    mock_token.credentials = "mocked_token"
    mock_request_data = {
        "name": "Test Publication",  
        "difficulty": "easy",
        "distance": -10.5,  
        "duration": 120,
        "price": 15.0,
        "description": "Test description",
        "tools": "None",
        "type": "public",
        "languages": ["english", "spanish"],
        "max_participants": 20,
        "dates": ["12-02-2025", "13-02-2025"],
        "country": "Test Country",
        "administrative_area_level_1": "Test State",
        "locality": "Test City"
    }
    mock_files = {
        "images": ("test_image.jpg", b"file_content", "image/jpeg")
    }

    with patch.object(PublicationService, "create", side_effect=HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")) as mock_create:

        with open(mock_files["images"][0], "wb") as file:
            file.write(mock_files["images"][1])
        files = {"images": (mock_files["images"][0], open(mock_files["images"][0], "rb"), mock_files["images"][2])}

        with pytest.raises(RequestValidationError) as e:
            client.post(
                "/api/",
                data=mock_request_data,
                files=files,
                headers={"Authorization": f"Bearer {mock_token.credentials}"}
            )

        error_detail = e.value.errors()
        assert error_detail[0]["loc"] == ("body", "distance")
        assert error_detail[0]["msg"] == "Input should be greater than 0"

        
