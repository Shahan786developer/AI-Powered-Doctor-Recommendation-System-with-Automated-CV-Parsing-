import os
from django.shortcuts import render, redirect
from .forms import CVUploadForm
from .models import *
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CVUploadForm
from .models import CV
from docx import Document


import openai

from django.shortcuts import render, redirect
from .forms import CVUploadForm
from .models import CV



import openai

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Registration view
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # Save the user to the database
                return redirect('login')  # Redirect to login page
            except Exception as e:
                # Log the error for debugging
                print(f"Error saving user: {e}")
                return render(request, 'resume/register.html', {'form': form, 'error': 'User could not be saved. Please try again.'})
        else:
            return render(request, 'resume/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'resume/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Check if the user has a profile
                if Profile.objects.filter(user=user).exists():
                    # Redirect to the profile page
                    return redirect('profile', user_id=user.id)
                else:
                    # Redirect to the home page
                    return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'resume/login.html', {'form': form})
def logout_view(request):
    logout(request)
    # Redirect to the login page after logging out
    return redirect('login')    

# Set OpenAI API key directly in views.py
OPENAI_API_KEY = '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'  # Replace with your actual OpenAI API key
import os
import json
import pdfplumber

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        # Return JSON response with error details if PDF extraction fails
        return json.dumps({"error": f"Error extracting PDF text: {e}"})
    return text.strip()

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext != '.pdf':
        return json.dumps({"error": "Unsupported file format. Only PDF files are allowed."})
    
    text = extract_text_from_pdf(file_path)
    
    # If the extract_text_from_pdf function returns a JSON error, return it immediately.
    try:
        # Attempt to load the text as JSON; if it loads, it means an error was returned.
        json.loads(text)
        # If we reached here, text is a valid JSON string (an error), so return it.
        return text
    except Exception:
        # Not a JSON error, so continue.
        pass
    
    if not text.strip():
        return json.dumps({"error": "No text extracted. Please check the file content."})
    
    return text

import openai
import json

def get_ai_recommendation(cv_text):
    openai.api_key = OPENAI_API_KEY  

    prompt = f"""
Extract the following details from the CV text of a doctor and output **only valid JSON with no additional text or commentary**.

Details to extract:
1. Name
2. Email
3. Phone Number
4. Degree (e.g., MBBS, MD)
5. Hobbies
6. Work Experience (include roles and exact years such as '2015-2020' or '5 years' if mentioned)
7. Specialization Skills (e.g., Cardiology, Dermatology, etc.)
8. PMC Number (Pakistan Medical Commission License Number, if present)
9. AI Recommendation (Assess how competent this person is based on their CV)

CV text:
{cv_text}

Return the answer in the exact JSON format below:
{{
    "name": "<Extracted Name>",
    "email": "<Extracted Email>",
    "phone": "<Extracted Phone Number>",
    "degree": "<Extracted Degree>",
    "hobbies": "<Extracted Hobbies>",
    "work_experience": "<Extracted Work Experience>",
    "skills": "<Extracted Skills>",
    "pmc_number": "<Extracted PMC Number>",
    "AI_Recommendation": "<AI Recommendation>"
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": "You are an AI that extracts and analyzes CVs for medical professionals."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000
        )

        ai_response = response['choices'][0]['message']['content'].strip()
        print("AI raw response:", ai_response)  # Debug: Check the raw output

        # Clean up any markdown formatting (e.g., remove ```json and ```)
        if ai_response.startswith("```"):
            # Remove starting and ending backticks
            ai_response = ai_response.strip("`")
            # Remove a language tag if present (like "json")
            if ai_response.lower().startswith("json"):
                ai_response = ai_response[len("json"):].strip()
        
        # Parse the JSON response
        extracted_info = json.loads(ai_response)

    except Exception as e:
        print(f"Error parsing AI response: {e}")
        extracted_info = {
            "name": "Not Extracted",
            "email": "Not Extracted",
            "phone": "Not Extracted",
            "degree": "Not Extracted",
            "hobbies": "Not Extracted",
            "work_experience": "Not Extracted",
            "skills": "Not Extracted",
            "pmc_number": "Not Extracted",
            "AI_Recommendation": "Not Extracted"
        }

    return extracted_info
# View for CV upload and processing


@login_required
@login_required
def upload_cv(request):
    # Fetch the user's profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded CV file
            uploaded_file = request.FILES['cv_file']
            cv_instance = CV(cv_file=uploaded_file)
            cv_instance.save()

            # Extract text from the uploaded CV
            file_path = cv_instance.cv_file.path
            extracted_text = extract_text(file_path)

            # Get AI-based extracted information from the CV
            ai_data = get_ai_recommendation(extracted_text)

            # Update the profile with the new CV and details
            profile.cv_file = cv_instance.cv_file
            profile.name = ai_data.get('name', 'None')
            profile.email = ai_data.get('email', 'None')
            profile.phone = ai_data.get('phone', 'None')
            profile.degree = ai_data.get('degree', 'None')
            profile.hobbies = ai_data.get('hobbies', 'None')
            profile.work_experience = ai_data.get('work_experience', 'None')
            profile.ai_recommendation = ai_data.get('AI_Recommendation', 'None')
            profile.pmc_number = ai_data.get('pmc_number', 'None')

            # Process the skills field from the AI response
            skills_value = ai_data.get('skills', '')
            if isinstance(skills_value, list):
                specialization_skills = skills_value
            elif isinstance(skills_value, str):
                specialization_skills = skills_value.split(',')
            else:
                specialization_skills = []

            # Clear previous skills before adding new ones
            profile.skills.clear()

            for skill_name in specialization_skills:
                # Ensure each skill is a string and strip any extra spaces
                if isinstance(skill_name, str):
                    skill_name = skill_name.strip()
                else:
                    skill_name = str(skill_name).strip()
                if skill_name:
                    skill, _ = Skill.objects.get_or_create(name=skill_name)
                    profile.skills.add(skill)

            profile.save()

            # Redirect to profile view after successful upload
            return redirect('profile', user_id=request.user.id)
    else:
        form = CVUploadForm()

    return render(request, 'resume/upload_cv.html', {
        'form': form,
        'profile': profile,
    })

@login_required
def cv_update(request):
    # Ensure the user has a profile
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return redirect('home')  # Redirect to home if no profile exists

    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new uploaded CV file
            uploaded_file = request.FILES['cv_file']
            cv_instance = CV(cv_file=uploaded_file)
            cv_instance.save()

            # Extract text from the uploaded CV
            file_path = cv_instance.cv_file.path
            extracted_text = extract_text(file_path)

            # Get AI-based extracted information from the CV
            ai_data = get_ai_recommendation(extracted_text)

            # Update the profile with the new CV and details
            profile.cv_file = cv_instance.cv_file
            profile.name = ai_data.get('name', 'None')
            profile.email = ai_data.get('email', 'None')
            profile.phone = ai_data.get('phone', 'None')
            profile.degree = ai_data.get('degree', 'None')
            profile.hobbies = ai_data.get('hobbies', 'None')
            profile.work_experience = ai_data.get('work_experience', 'None')
            profile.ai_recommendation = ai_data.get('AI_Recommendation', 'None')
            profile.pmc_number = ai_data.get('pmc_number', 'None')

            # Process the skills field from the AI response
            skills_value = ai_data.get('skills', '')
            if isinstance(skills_value, list):
                specialization_skills = skills_value
            elif isinstance(skills_value, str):
                specialization_skills = skills_value.split(',')
            else:
                specialization_skills = []

            # Clear previous skills before adding new ones
            profile.skills.clear()

            # Add new skills
            for skill_name in specialization_skills:
                # Ensure each skill is a string and strip any extra spaces
                if isinstance(skill_name, str):
                    skill_name = skill_name.strip()
                else:
                    skill_name = str(skill_name).strip()
                if skill_name:
                    skill, _ = Skill.objects.get_or_create(name=skill_name)
                    profile.skills.add(skill)

            # Save the updated profile
            profile.save()

            # Redirect to profile view
            return redirect('profile', user_id=request.user.id)
    else:
        form = CVUploadForm()

    return render(request, 'resume/update_cv.html', {'form': form, 'profile': profile})


@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    return render(request, 'resume/profile.html', {
        'profile': profile
    })
@login_required
def dashboard(request):
    # Fetch any additional data required for the dashboard
    return render(request, 'resume/dashboard.html', {})

# View for success page after CV upload
def success(request, cv_id):
    cv_instance = get_object_or_404(CV, id=cv_id)
    return render(request, 'resume/success.html', {'cv': cv_instance})


# View to display extracted information
@login_required
def extracted_info_view(request, extracted_info_id):
    # Fetch the CV instance
    cv_instance = get_object_or_404(CV, id=extracted_info_id)

    # Retrieve the logged-in user's profile details
    profile = get_object_or_404(Profile, user=request.user)

    # Pass the profile data to the template
    return render(request, 'resume/extracted_info.html', {
        'cv': cv_instance,
        'profile': profile
    })
