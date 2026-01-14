# RepCounter

A Python application that uses computer vision and machine learning to count exercise repetitions via webcam. Trained with an SVM classifier to recognize arm positions (extended vs contracted).

## Features

- Real-time rep counting using camera input
- Machine learning-based pose detection (SVM classifier)
- Exercise tracking and rep counting
- Data collection interface for training
- Easy-to-use Tkinter GUI

## Installation

### Prerequisites
- Python 3.9 or higher
- Webcam
- macOS, Linux, or Windows

### Setup

1. Clone the repository:
```bash
git clone https://github.com/zaynganiev/RepCounter.git
cd RepCounter
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### How to Use

1. **Collect Training Data:**
   - Click "Extended" button multiple times to capture images of your extended arm position
   - Click "Contracted" button multiple times to capture images of your contracted arm position
   - Aim for 10+ images per position for good model accuracy

2. **Train the Model:**
   - Click "Train Model" to train the SVM classifier on your collected images
   - Check terminal output for confirmation message

3. **Count Reps:**
   - Click "Toggle Counting" to enable rep counting
   - Perform your exercises - reps will increment when the model detects a complete extension-to-contraction cycle
   - Click "Reset" to reset the counter

## Project Structure

- `main.py` - Entry point
- `app.py` - Main GUI application with rep counting logic
- `camera.py` - Camera input and frame capture
- `model.py` - Machine learning model (SVM) for pose classification
- `requirements.txt` - Python dependencies

## Technical Details

- **ML Framework:** scikit-learn (LinearSVC)
- **GUI:** Python Tkinter
- **Computer Vision:** OpenCV
- **Image Processing:** Pillow

## Troubleshooting

- **Camera not found:** Check that your webcam is properly connected and not in use by other applications
- **Poor rep detection:** Collect more training images in good lighting conditions
- **Model training fails:** Ensure you have collected images for both positions

## Future Improvements

- Support for multiple exercise types
- Adjustable sensitivity settings
- Rep history and statistics tracking
- Video recording capability

## License

[Add your license here]

## Author

Zayn Ganiev
