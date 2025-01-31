# Satellite Image Capture and Object Recognition

This project consists of two main components:

1. **Download Module:**  
   The application allows you to download satellite images using the Google Maps API by providing geographic coordinates. By default, the images are downloaded every 5 km (this distance can be adjusted in the code). The zoom level of the images is customizable.

2. **Detection Module:**  
   The application processes the downloaded images to detect circular shapes using pre-trained models. The models are sourced from [Roboflow Universe](https://universe.roboflow.com/). If you wish to change the detection model, you can do so through the code.

Additionally, the application features a **Streamlit-based GUI** to simplify usage for the final user. Many advanced parameters are adjustable only through the code to ensure the interface remains user-friendly.

---

## **Prerequisites**

1. **Python 3.8 or later** installed.
2. A **valid Google Maps API Key** (with access to the Static Maps API enabled).
3. Internet connection.

---

## **Steps to Obtain a Google Maps Static API Key**

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **Static Maps API**.
3. Generate an API Key and ensure it has permission to access the Static Maps service.
4. Copy the API Key and provide it when running the application.

---

## **Installation Steps**

1. Clone this repository or download the files:

    ```bash
    git clone https://github.com/your_user/satellite-download-and-detect.git
    cd satellite-download-and-detect
    ```

2. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## **How to Run the Application**

1. From the terminal, run the following command inside the project directory:

    ```bash
    streamlit run app.py
    ```

2. A web interface will open in your browser.

---

## **How to Use the Application**

1. **API Key:** Enter your Google Maps API Key in the sidebar.
2. **Detection Model:** Select the object detection model you want to use.
3. **Provide Geographic Coordinates:** Specify the minimum and maximum latitude and longitude of the area you want to download.
4. **Download Images:** The application will download satellite images within the specified area.
5. **Process Images:** Once the images are downloaded, press the button to process them and detect objects.  

**Note:** The processed images will have bounding boxes drawn around detected objects, and a **CSV file** will be generated with details about each detection, such as location, size, and confidence.

All generated data will be stored in an automatically created output folder within the project directory.

### **Understanding the CSV File and Locating Detected Objects in Google Maps**

The generated **CSV** file contains details about the detected objects in each image. Below is an explanation of the columns:

| Column              | Description                                                                                       |
|--------------------|---------------------------------------------------------------------------------------------------|
| **Imagen**          | The name of the image file containing the detection. This name includes the coordinates of the area. |
| **Latitud Mínima**  | The minimum latitude of the area covered by the image.                                            |
| **Longitud Mínima** | The minimum longitude of the area covered by the image.                                           |
| **Latitud Máxima**  | The maximum latitude of the area covered by the image.                                            |
| **Longitud Máxima** | The maximum longitude of the area covered by the image.                                           |
| **x**               | The x-coordinate of the center of the detected object within the image.                          |
| **y**               | The y-coordinate of the center of the detected object within the image.                          |
| **Ancho**           | The width of the bounding box around the detected object in pixels.                              |
| **Alto**            | The height of the bounding box around the detected object in pixels.                             |
| **Confianza**       | The confidence score of the detection (a value between 0 and 1, where 1 indicates high certainty).|
| **Clase**           | The category or label of the detected object (e.g., "tomb").                                      |
| **Latitud Objeto**  | **The precise latitude of the detected object within the area.**                                  |
| **Longitud Objeto** | **The precise longitude of the detected object within the area.**                                 |

**How to Use the Object Coordinates**
The precise latitude and longitude of each detected object can be used to directly locate it in **Google Maps**.

---

## **Project Structure**

```
/satellite-download-and-detect
├── app.py                   # Main Streamlit application
├── config.py                # Configuration for directories and models
├── inference_config.py      # Creation of the client communicating with Roboflow
├── download_img.py          # Satellite image downloading logic
├── draw_bounding_box.py     # Image processing and object detection
├── requirements.txt         # List of dependencies
├── README.md                # Project documentation
└── outputs/                 # Output folder for processed images
```
---

## **Important Notes**

For the final user of this application, it is important to clarify that different detection models work best depending on the zoom level of the images:

- **Default Model (`googleearthtomb/12`):**  
  This model is the most reliable according to tests and works well for images with medium zoom (around 16).
  
![WhatsApp Image 2025-01-31 at 18 03 57](https://github.com/user-attachments/assets/46186706-2561-41da-a21c-e5f979c35d6d)

  
- **Model `710robotrain/3`:**  
  This model works better for distant images (zoom around 17).
  
![WhatsApp Image 2025-01-31 at 16 33 22](https://github.com/user-attachments/assets/923ccdb8-23f7-4db7-ae09-93425e8213a2)

  
- **Model `circulos-gcomj/31`:**  
  Ideal for high-zoom images where circular objects occupy most of the image.
  
![WhatsApp Image 2025-01-31 at 14 38 26](https://github.com/user-attachments/assets/16359c9c-93d4-464a-9b63-b5342621eadd)


---

## **License**

This project is licensed under the MIT License, allowing free modification and distribution.
