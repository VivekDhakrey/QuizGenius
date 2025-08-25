import json
import os
import google.generativeai as genai

class QuizGenerator:
    def __init__(self, api_key):
        """Initialize the quiz generator with Gemini API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_quiz(self, text_content, num_mcq=5, num_tf=5, difficulty="Medium"):
        """
        Generate quiz questions from text content
        
        Args:
            text_content (str): The processed text content
            num_mcq (int): Number of multiple choice questions
            num_tf (int): Number of true/false questions
            difficulty (str): Difficulty level (Easy, Medium, Hard)
        
        Returns:
            dict: Generated quiz data with multiple choice and true/false questions
        """
        # Generate multiple choice questions
        mcq_questions = self._generate_multiple_choice(text_content, num_mcq, difficulty)
        
        # Generate true/false questions
        tf_questions = self._generate_true_false(text_content, num_tf, difficulty)
        
        return {
            "multiple_choice": mcq_questions,
            "true_false": tf_questions,
            "metadata": {
                "difficulty": difficulty,
                "total_questions": num_mcq + num_tf,
                "source_length": len(text_content)
            }
        }
    
    def _generate_multiple_choice(self, text_content, num_questions, difficulty):
        """Generate multiple choice questions"""
        prompt = f"""
        Based on the following text content, generate exactly {num_questions} multiple choice questions at {difficulty} difficulty level.
        
        Requirements:
        - Each question should have exactly 4 options (A, B, C, D)
        - Only one option should be correct
        - Include an explanation for why the correct answer is right
        - Questions should test comprehension, not just memorization
        - Avoid questions that can be answered without reading the text
        - Make sure all questions are directly answerable from the provided content
        
        Text content:
        {text_content[:4000]}  # Limit content to avoid token limits
        
        Response format (JSON only):
        {{
            "questions": [
                {{
                    "question": "Question text here?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option B",
                    "explanation": "Explanation of why this is correct"
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2000,
                )
            )
            
            # Extract and clean JSON from response
            response_text = response.text.strip()
            
            # Try to find and extract JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_text = response_text[json_start:json_end]
                
                # Clean up common JSON formatting issues
                json_text = json_text.replace('\n', ' ')
                json_text = json_text.replace('\t', ' ')
                # Remove multiple spaces
                import re
                json_text = re.sub(r'\s+', ' ', json_text)
                
                try:
                    result = json.loads(json_text)
                    return result.get("questions", [])
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract questions manually
                    return self._extract_questions_manually(response_text, "mcq")
            else:
                return self._extract_questions_manually(response_text, "mcq")
            
        except Exception as e:
            raise Exception(f"Failed to generate multiple choice questions: {str(e)}")
    
    def _generate_true_false(self, text_content, num_questions, difficulty):
        """Generate true/false questions"""
        prompt = f"""
        Based on the following text content, generate exactly {num_questions} true/false questions at {difficulty} difficulty level.
        
        Requirements:
        - Questions should be clearly true or false based on the content
        - Include an explanation for the correct answer
        - Mix of true and false answers (roughly 50/50)
        - Questions should test understanding, not just factual recall
        - Avoid ambiguous statements
        - Make sure all questions are directly answerable from the provided content
        
        Text content:
        {text_content[:4000]}  # Limit content to avoid token limits
        
        Response format (JSON only):
        {{
            "questions": [
                {{
                    "question": "Statement to evaluate as true or false",
                    "correct_answer": true,
                    "explanation": "Explanation of why this is true/false"
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2000,
                )
            )
            
            # Extract and clean JSON from response
            response_text = response.text.strip()
            
            # Try to find and extract JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_text = response_text[json_start:json_end]
                
                # Clean up common JSON formatting issues
                json_text = json_text.replace('\n', ' ')
                json_text = json_text.replace('\t', ' ')
                # Remove multiple spaces
                import re
                json_text = re.sub(r'\s+', ' ', json_text)
                
                try:
                    result = json.loads(json_text)
                    return result.get("questions", [])
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract questions manually
                    return self._extract_questions_manually(response_text, "tf")
            else:
                return self._extract_questions_manually(response_text, "tf")
            
        except Exception as e:
            raise Exception(f"Failed to generate true/false questions: {str(e)}")
    
    def validate_quiz_data(self, quiz_data):
        """Validate the generated quiz data structure"""
        required_keys = ["multiple_choice", "true_false"]
        
        for key in required_keys:
            if key not in quiz_data:
                raise ValueError(f"Missing required key: {key}")
        
        # Validate multiple choice questions
        for mcq in quiz_data["multiple_choice"]:
            required_mcq_keys = ["question", "options", "correct_answer"]
            for req_key in required_mcq_keys:
                if req_key not in mcq:
                    raise ValueError(f"Missing required key in MCQ: {req_key}")
            
            if len(mcq["options"]) != 4:
                raise ValueError("Multiple choice questions must have exactly 4 options")
            
            if mcq["correct_answer"] not in mcq["options"]:
                raise ValueError("Correct answer must be one of the provided options")
        
        # Validate true/false questions
        for tf in quiz_data["true_false"]:
            required_tf_keys = ["question", "correct_answer"]
            for req_key in required_tf_keys:
                if req_key not in tf:
                    raise ValueError(f"Missing required key in T/F: {req_key}")
            
            if not isinstance(tf["correct_answer"], bool):
                raise ValueError("True/false correct_answer must be a boolean")
        
        return True
    
    def _extract_questions_manually(self, response_text, question_type):
        """Fallback method to extract questions when JSON parsing fails"""
        questions = []
        
        if question_type == "mcq":
            # Try to extract multiple choice questions manually
            # This is a simple fallback - look for patterns
            lines = response_text.split('\n')
            current_question = None
            current_options = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('Question') or line.endswith('?'):
                    if current_question and current_options:
                        questions.append({
                            "question": current_question,
                            "options": current_options[:4],  # Limit to 4 options
                            "correct_answer": current_options[0] if current_options else "",
                            "explanation": "No explanation available"
                        })
                    current_question = line
                    current_options = []
                elif line and (line.startswith(('A.', 'B.', 'C.', 'D.', '1.', '2.', '3.', '4.'))):
                    # Extract option text
                    option_text = line[2:].strip() if len(line) > 2 else line
                    current_options.append(option_text)
            
            # Add the last question if exists
            if current_question and current_options:
                questions.append({
                    "question": current_question,
                    "options": current_options[:4],
                    "correct_answer": current_options[0] if current_options else "",
                    "explanation": "No explanation available"
                })
        
        elif question_type == "tf":
            # Try to extract true/false questions manually
            lines = response_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.endswith('?') or 'True' in line or 'False' in line:
                    if line:
                        questions.append({
                            "question": line,
                            "correct_answer": True,  # Default to True
                            "explanation": "No explanation available"
                        })
        
        return questions[:5]  # Limit to 5 questions as fallback
