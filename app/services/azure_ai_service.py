"""
Azure AI Services integration for SafeWayAI application.
This module provides functionality to interact with Azure Cognitive Services.
"""

import os
import logging
import json
import requests
import azure.cognitiveservices.speech as speechsdk
from app.config.azure_config import AI_SERVICES_CONFIG

logger = logging.getLogger(__name__)

class AzureAIService:
    """Service for interacting with Azure AI services."""
    
    def __init__(self):
        """Initialize the Azure AI service."""
        self.speech_key = AI_SERVICES_CONFIG["speech_key"]
        self.speech_region = AI_SERVICES_CONFIG["speech_region"]
        self.vision_key = AI_SERVICES_CONFIG["vision_key"]
        self.vision_endpoint = AI_SERVICES_CONFIG["vision_endpoint"]
        logger.info("Azure AI service initialized")
    
    def text_to_speech(self, text, output_file=None):
        """
        Convert text to speech using Azure Speech Service.
        
        Args:
            text (str): The text to convert to speech
            output_file (str, optional): Path to save the audio file
            
        Returns:
            bytes or str: Audio data or path to saved file
        """
        try:
            # Configure speech service
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                region=self.speech_region
            )
            
            # Set voice
            speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
            
            # Determine output
            if output_file:
                audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=speech_config, 
                    audio_config=audio_config
                )
                result = synthesizer.speak_text_async(text).get()
                
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    logger.info(f"Speech synthesized and saved to {output_file}")
                    return output_file
                else:
                    logger.error(f"Speech synthesis failed: {result.reason}")
                    return None
            else:
                # Stream the audio
                synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
                result = synthesizer.speak_text_async(text).get()
                
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    logger.info("Speech synthesized successfully")
                    return result.audio_data
                else:
                    logger.error(f"Speech synthesis failed: {result.reason}")
                    return None
                
        except Exception as e:
            logger.error(f"Error in text to speech conversion: {e}")
            return None
    
    def speech_to_text(self, audio_file=None):
        """
        Convert speech to text using Azure Speech Service.
        
        Args:
            audio_file (str, optional): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        try:
            # Configure speech service
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                region=self.speech_region
            )
            
            # Set up audio input
            if audio_file:
                audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
            else:
                # Use default microphone if no file provided
                audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            
            # Create recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, 
                audio_config=audio_config
            )
            
            # Start recognition
            logger.info("Recognizing speech...")
            result = speech_recognizer.recognize_once_async().get()
            
            # Process result
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"Speech recognized: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning("No speech could be recognized")
                return ""
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Speech recognition canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                return None
                
        except Exception as e:
            logger.error(f"Error in speech to text conversion: {e}")
            return None
    
    def analyze_image(self, image_path=None, image_url=None, features=None):
        """
        Analyze an image using Azure Computer Vision.
        
        Args:
            image_path (str, optional): Path to the image file
            image_url (str, optional): URL of the image
            features (list, optional): List of features to analyze
            
        Returns:
            dict: Analysis results
        """
        try:
            if not features:
                features = ["Description", "Objects", "Tags"]
                
            # Set up the API endpoint
            analyze_url = f"{self.vision_endpoint}vision/v3.2/analyze"
            
            # Set up headers
            headers = {
                'Ocp-Apim-Subscription-Key': self.vision_key,
                'Content-Type': 'application/json' if image_url else 'application/octet-stream'
            }
            
            # Set up parameters
            params = {
                'visualFeatures': ','.join(features),
                'language': 'en'
            }
            
            # Prepare the request body
            if image_url:
                body = {'url': image_url}
                response = requests.post(
                    analyze_url, 
                    headers=headers, 
                    params=params, 
                    json=body
                )
            else:
                # Read the image file
                with open(image_path, 'rb') as image_data:
                    response = requests.post(
                        analyze_url, 
                        headers=headers, 
                        params=params, 
                        data=image_data.read()
                    )
            
            # Check response
            response.raise_for_status()
            
            # Return analysis results
            return response.json()
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {"error": str(e)}
    
    def detect_emergency_from_audio(self, audio_file=None):
        """
        Detect emergency situations from audio.
        
        This would use speech recognition to transcribe audio and then
        analyze the text for emergency keywords or distress signals.
        
        Args:
            audio_file (str, optional): Path to the audio file
            
        Returns:
            dict: Emergency detection results
        """
        try:
            # First, convert speech to text
            transcribed_text = self.speech_to_text(audio_file)
            
            if not transcribed_text:
                return {
                    "emergency_detected": False,
                    "confidence": 0,
                    "message": "No speech detected"
                }
            
            # Define emergency keywords
            emergency_keywords = [
                "help", "emergency", "danger", "attack", "fire",
                "hurt", "injured", "bleeding", "pain", "accident",
                "assault", "robbery", "threat", "weapon", "gun",
                "knife", "dying", "collapse", "unconscious", "heart attack",
                "stroke", "choking", "drowning", "fall", "crash"
            ]
            
            # Check for emergency keywords
            detected_keywords = []
            for keyword in emergency_keywords:
                if keyword.lower() in transcribed_text.lower():
                    detected_keywords.append(keyword)
            
            # Calculate confidence based on number of keywords detected
            confidence = min(len(detected_keywords) * 0.2, 1.0)
            
            # Determine if this is an emergency
            is_emergency = confidence > 0.3
            
            return {
                "emergency_detected": is_emergency,
                "confidence": confidence,
                "detected_keywords": detected_keywords,
                "transcribed_text": transcribed_text,
                "message": "Emergency detected" if is_emergency else "No emergency detected"
            }
            
        except Exception as e:
            logger.error(f"Error detecting emergency from audio: {e}")
            return {
                "emergency_detected": False,
                "confidence": 0,
                "message": f"Error: {str(e)}"
            }
    
    def detect_emergency_from_image(self, image_path=None, image_url=None):
        """
        Detect emergency situations from images.
        
        This would analyze images for signs of emergencies like fires,
        accidents, injuries, etc.
        
        Args:
            image_path (str, optional): Path to the image file
            image_url (str, optional): URL of the image
            
        Returns:
            dict: Emergency detection results
        """
        try:
            # Analyze the image
            analysis = self.analyze_image(
                image_path=image_path, 
                image_url=image_url,
                features=["Description", "Objects", "Tags"]
            )
            
            if "error" in analysis:
                return {
                    "emergency_detected": False,
                    "confidence": 0,
                    "message": f"Error: {analysis['error']}"
                }
            
            # Define emergency-related tags
            emergency_tags = [
                "fire", "smoke", "accident", "injury", "blood",
                "weapon", "gun", "knife", "fight", "crash",
                "ambulance", "police", "emergency", "danger", "disaster",
                "explosion", "collapsed", "unconscious", "wound", "damage"
            ]
            
            # Check for emergency tags in the analysis
            detected_tags = []
            
            # Check tags
            if "tags" in analysis:
                for tag in analysis["tags"]:
                    if tag["name"].lower() in emergency_tags:
                        detected_tags.append({
                            "name": tag["name"],
                            "confidence": tag["confidence"]
                        })
            
            # Check objects
            if "objects" in analysis:
                for obj in analysis["objects"]:
                    if obj["object"].lower() in emergency_tags:
                        detected_tags.append({
                            "name": obj["object"],
                            "confidence": obj["confidence"]
                        })
            
            # Check description
            if "description" in analysis and "captions" in analysis["description"]:
                for caption in analysis["description"]["captions"]:
                    for tag in emergency_tags:
                        if tag in caption["text"].lower():
                            detected_tags.append({
                                "name": tag,
                                "confidence": caption["confidence"]
                            })
            
            # Calculate overall confidence
            if detected_tags:
                # Average confidence of detected tags
                avg_confidence = sum(tag["confidence"] for tag in detected_tags) / len(detected_tags)
            else:
                avg_confidence = 0
            
            # Determine if this is an emergency
            is_emergency = avg_confidence > 0.6
            
            return {
                "emergency_detected": is_emergency,
                "confidence": avg_confidence,
                "detected_tags": detected_tags,
                "message": "Emergency detected" if is_emergency else "No emergency detected",
                "analysis_summary": analysis.get("description", {}).get("captions", [{}])[0].get("text", "")
            }
            
        except Exception as e:
            logger.error(f"Error detecting emergency from image: {e}")
            return {
                "emergency_detected": False,
                "confidence": 0,
                "message": f"Error: {str(e)}"
            }
