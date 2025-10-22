# 3M Lighting Consumer Video Analysis - Configuration
# Updated: October 21, 2025

PROCESSING_CONFIG = {
    # Processing tier: FREE (local only), PLUS (hybrid), PRO (max quality)
    'tier': 'PLUS',
    
    # Minimum confidence threshold for including insights (0.0 to 1.0)
    'confidence_threshold': 0.75,
    
    # Priority questions from discussion guide (1-11)
    'priority_questions': [3, 7, 8],
    
    # Focus areas (ranked by importance)
    'focus_areas': [
        'pain_points',
        '3m_adjacency',
        'golden_moments',
        'workarounds'
    ],
    
    # Emotion sensitivity: low, medium, high
    'emotion_sensitivity': 'high',
    
    # Quote selection preference: 'impactful' or 'representative'
    'quote_preference': 'impactful',
    
    # Video processing settings
    'frame_sample_interval': 5,  # seconds between frame samples
    'emotion_window': 5,  # seconds for emotion-JTBD alignment
    
    # Output settings
    'max_quotes_per_category': 20,
    'max_pain_points': 7,
    'generate_html_visualization': True
}

# Model paths
MODEL_PATHS = {
    'qwen': '/Volumes/TARS/llm-models/qwen2.5-vl-7b-instruct',
    'whisper': 'large-v3-turbo',
    'hubert': '/Volumes/TARS/llm-models/hubert-large'
}

# Directory structure
PATHS = {
    'raw_videos': '/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/raw-videos',
    'processed': '/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/processed',
    'outputs': '/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/outputs',
    'logs': '/Users/anderson115/00-interlink/12-work/3m-lighting-project/modules/consumer-video/data/logs'
}

# Media source (read-only)
MEDIA_SOURCE = '/Volumes/DATA/consulting/3m-lighting-consumer-videos/Intro Videos'
