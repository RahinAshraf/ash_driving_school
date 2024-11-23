from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from itertools import chain




# View to render abu.html
def abu_view(request):
    return render(request, "abu.html")


def reviews_view(request):
    # Predefined static list of reviews \n\n
    static_reviews  = [
        {
            'user': 'frank woodford',
            'rating': 5,
            'comment': 'My experience was very good with Abu Ashraf as he made me feel very comfortable which allowed me to pass today, thank you Abu Ashraf',
            'created_at': '28th Oct 2024',
        },
        {
            'user': 'khadija Guebli',
            'rating': 5,
            'comment': 'i passed for the first time today! \n\ni had been learning with abu ashraf for a total of 6 months and they were probably the best months ever! abu ensured that every single lesson we had together was full of laughter but also seriousness, a good balance of the two resulted with our lessons never being boring. \n\nabu always remained patient and made sure i always understood what he would teach me and if i didn’t understand something he would go over it again until i did. i also had a few gaps whilst i was learning how to drive as i went on holiday and i’m currently at university so i’ve moved away. \n\ni had a 3 week nearly 4 week gap but i did back to back lessons for 4 days straight with abu and it was more than enough for me to pass! abu ashraf is an amazing instructor who will definitely secure you a straight pass.',
            'created_at': '19th Nov 2024',
        },
        {
            'user': 'Adekunle David Afolabi',
            'rating': 5,
            'comment': "I’m David Afolabi and I took my driving lessons with Abu Ashraf. All I can say is that he’s the best tutor in the UK. He’s so patient and teaches you like you are a five year old. He took me round all test routes and he was just the best. \n\nI passed my driving test at one go with just minor fault. My wife equally passed her test with him with one minor fault. If you are looking for an instructor who is well detailed and pays attention to details then Abu Ashraf is you go to person. 5 star rating for him.",
            'created_at': '19th Oct 2024',
        },
        {
            'user': 'Tam Nguyen',
            'rating': 5,
            'comment': 'I passed my driving test, with Abu Ashraf as my instructor. This is my first attempt at driving test. \n\nI strongly recommend him for anyone looking for driving lessons. I came to Ashraf about 5 months before my test. I tried a few instructors before, but they made me feel quite unsafe and I was not learning anything properly, so I stopped my lessons with them. On my first day with Ashraf, he immediately proved himself as a knowledgeable, pedagogical, and dedicated instructor. \n\nI was very impressed. Then for 5 months we took lessons, twice a week and more frequently in the leadup to my test. He walked me through everything, explaining everything carefully and offering a lot of encouragement along the way. I will miss Abu Ashraf a lot in the future when I will be driving my own car, without him sitting next to me. He has prepared me for a lifetime of safe driving, for which I cannot thank him enough!',
            'created_at': '14th Oct 2024',
        },{
            'user': 'aregbesola olayinka',
            'rating': 5,
            'comment': 'I took my Driving lessons with Abu Ashraf 17 hours in total and he was just too good. He took me through all the test routes within St Albans and one of the test routes he reviewed with me 20mins before the test was the one taken by the examiner. \n\nHe explains the rules to you like he explaining to a 5 years old just to ensure you understand them .I just too happy now.I passed the the test on my first attempt!!',
            'created_at': '9th Sep 2024',
        },{
            'user': 'oluwasegun ogunbanjo',
            'rating': 5,
            'comment': "I wanted to express my deepest gratitude to Abu Ashraf for your outstanding tutoring, not just for myself, but also for my two brothers. \n\nYour dedication, expertise, and patience have truly made all the difference, and thanks to you, we all passed our exams on the first attempt with only one minor fault—an incredible achievement we couldn’t have reached without your guidance. What amazes us the most is your impressive knowledge of the St. Alban's area. It’s as if you have the map of the city ingrained in your mind, always knowing the best routes and how to navigate the streets with ease. Your understanding of the area and your calm, encouraging teaching style gave us the confidence we needed to succeed. We are truly fortunate to have had you as our instructor, and we cannot thank you enough for your dedication and support once again Abu Ashraf you are the best.",
            'created_at': '25th Sep 2024',
        },{
            'user': 'Lawal',
            'rating': 5,
            'comment': 'I passed my driving test today (13/06/2024) Am so excited this is over,felt very nervous going for this test.i nearly gave up during parallel parking today but I remember my instructor voice in my head during his teaching saying dont give up whenever you are doing any manoeuvres. \n\nAll thanks to my instructor Abu Ashraf for his good driving teachings.I recommend him 100percent,my husband passed with him too.Am confident to recommend him to anyone.He is super good 💯 👍',
            'created_at': '13th Jun 2024',
        },{
            'user': 'Samia Begum',
            'rating': 5,
            'comment': 'Thank you Abu Ashraf (Ash) for helping me pass my driving test with only one minor fault. He has been incredibly helpful ensuring I enter the test fully ready and confident. He covered every topic and would ensure that I go into the test with all my weaknesses covered. He has also given all his students the opportunity to sit at the back of his students lesson (free of charge) which also helped massively! \n\nI would highly recommend him for any students that want to pass in a short space of time!',
            'created_at': '14th Jul 2024',
        },{
            'user': 'Solomon Temidayo',
            'rating': 5,
            'comment': "I'm thrilled to share my exceptional experience with Abu Ashraf, an outstanding driving instructor in St Albans! With his expert guidance, I passed my driving test on the first attempt, and I couldn't be more grateful. Abu's teaching style is calm, patient, and tailored to your individual needs. He creates a supportive and relaxed learning environment, making even the most nervous students feel at ease. \n\nHis in-depth knowledge of the roads in St Albans and expert tips helped me navigate challenging situations with confidence. What sets Abu apart is his dedication, enthusiasm, and genuine interest in his students' progress. He's always punctual, professional, and willing to go the extra mile to ensure you're test-ready. If you're looking for a reliable and skilled driving instructor in St Albans, look no further than Abu Ashraf. His exceptional teaching skills and passion for driving will have you passing your test in no time! Five stars aren't enough – I'd give him ten if I could!",
            'created_at': '26th Aug 2024',
        },{
            'user': 'Blessing Pool',
            'rating': 5,
            'comment': 'Abu Ashraf helped me pass my driving test with just three lessons. He is an amazing instructor as he explains everything clearly and corrects mistakes with a positive attitude which really helps relieve any nervousness. I highly recommend Abu as a driving instructor. \n\nI have had other instructors in the past who were nowhere near as helpful! Thank you Abu Ashraf :)',
            'created_at': '20th May 2024',
        },{
            'user': 'EBERECHUKWU DOR NWAGBUO',
            'rating': 5,
            'comment': "I'm most grateful to Mr Abu Ashraf an outstanding instructor for the rescue mission he did concerning my knowledge and understanding to UK road system within a short period of time. \n\nAbu Ashraf is a born driver instructor who takes his time (in the rain & Cold) to break his teaching to the lowest term that a lay man can understand. Thank you Abu Ashraf for crossing my path to pass my driving test today. You are magical.",
            'created_at': '18th Mar 2024',
        },{
            'user': 'kanyinsola Daddah',
            'rating': 5,
            'comment': "I want to thank my instructor Abu Ashraf for instilling in me the courage I needed to pass my driving test .....I froze many times ,but he kept saying during my lessons 'dont give up' and I didnt give up......he was so patient and was always encouraging me. \n\nI would definitely recommend him to anyone who is determined to start their driving journey .....I passed my driving test today at my first attempt and I'm so happy.Thank you again Abu Ashraf .",
            'created_at': '23rd Jun 2024',
        },{
            'user': 'Lola Parratt',
            'rating': 5,
            'comment': "Wow! What an experience learning to drive and passing first time. Wouldn't never have been able to do it without my wonderful driver instructor Abu Ashraf. \n\nI started off so nervous never wanting to drive more than 20 Mph. But after time he installed so much confidence in me. I honestly couldn't have hoped for a better person to teach me how to drive. 100000/10!",
            'created_at': '30th May 2024',
        },{
            'user': 'Leila Matse-Orere',
            'rating': 5,
            'comment': "I had the privilege of taking lessons with Abu Ashraf and can't recommend him highly enough. His methodical and thorough teaching approach ensured that I was well-prepared in every aspect of my test. What truly sets him apart, though, is his patience and personable nature, which made each lesson enjoyable and stress-free. Thanks to him, I passed my test on the first attempt. \n\nIf you're seeking an instructor who genuinely cares about your success and goes the extra mile, Abu Ashraf is your guy! I owe my achievement entirely to his guidance.",
            'created_at': '14th Oct 2023',
        },{
            'user': "Natalie O'Shaughnessy",
            'rating': 5,
            'comment': 'Big thanks to Abu Ashraf for helping me pass first time. Ash took me on a couple of weeks before my test after my last instructor moved away. I was quite nervous about the test anyway but changing instructors and a different car just 2 weeks before the test was really on mind. \n\nAsh really helped to help me feel ready for the test despite the last minute changes. He’s helped me to become more confident in areas I was struggling with. He really patient and explains everything clearly!',
            'created_at': '27th Jun 2024',
        },{
            'user': 'Olayinka D.A',
            'rating': 5,
            'comment': 'This is about Abu Ashraf. My driving instructor was Amazing! He was very professional, meticulous and supportive. Mr Ash saw more potential in me than I did some times. He encouraged me and motivated me. While being very serious , he would throw in some jokes so that you can feel at ease. \n\nMr Ash is very competent and patient, he would teach until you feel you are confident enough to drive. He saw I had some weaknesses and taught me over and over again until I understood it. Mr Ash was dedicated to seeing me pass, I saw this dedication with other students too. I have recommended to everyone and I will still do. I am glad I had an amazing instructor like Mr Abu Ashraf.',
            'created_at': '25th Feb 2024',
        },{
            'user': 'Ashutosh Singh',
            'rating': 5,
            'comment': 'I had an exceptional experience learning to drive with Abu Ashraf. He accommodated my lessons on short notice, ensuring I was well-prepared for my test. His instructions were crystal clear, making even the trickiest maneuvers seem manageable. \n\nWhat impressed me the most was his patience. He remained calm and supportive, even when I made mistakes, which boosted my confidence behind the wheel. Thanks to him, I passed my driving test with flying colors. I highly recommend Abu Ashraf to anyone looking for a skilled and patient driving instructor.',
            'created_at': '5th May 2024',
        },{
            'user': 'Merlin Roy',
            'rating': 5,
            'comment': "I'm thrilled to share that I successfully passed my driving test on the first attempt, thanks to the excellent guidance of Abu Ashraf. His support, clear instructions, and wealth of knowledge played an important role in my success. \n\nI highly recommend him as a great instructor, and I'm truly grateful for his contribution to my achievement. Thank you, Abu Ashraf!",
            'created_at': '21st Nov 2023',
        },{
            'user': 'Augustus Nwokeiwu',
            'rating': 5,
            'comment': 'Wow! It was really great experience with my driving instructor (Abu Ashraf). He took his time to explain everything I needed to know to pass my driving test. To my greatest surprise, I pass my test at the first attempt. I strongly recommend him for your driving lessons.',
            'created_at': '22nd Jun 2024',
        },{
            'user': 'Melissa Sorby',
            'rating': 5,
            'comment': "I passed my test today after being taught by Abu Ashraf (Ash). Ash is an amazing instructor as he is so knowledgeable, but also patient and explains things very well. He doesn't just care about you passing your test, he cares about your safety on the road beyond passing. I passed with only 2 minors which is testament to Ash's emphasis on driving safely. I would recommend Ash to anyone!",
            'created_at': '9th Aug 2023',
        },{
            'user': 'Arun sundar',
            'rating': 5,
            'comment': 'I have been with Abu Ashraf for just 2 months and it was very helpful and he taught me driving all the routes in St. Albans and I’m very grateful to have such an instructor and a very supportive friend. With his guidance I passed my driving test. He usually gives me lot of driving materials, pictures which was quite interesting. \n\nBasically the mock test helps me a lot and overall his teaching is excellent and informative as well as supportive instructor. While driving He is good and relax and he keeps me in relax mode too. Thanks Abu',
            'created_at': '1st Nov 2023',
        },{
            'user': 'ibrahim',
            'rating': 5,
            'comment': "Abu Ashraf is an amazing instructor who helped me pass my driving test by thoroughly and clearly teaching me, helping me become an expert driver in no time! He's very patient and speaks and describes everything clearly allowing me to understand and comprehend everything. \n\nit was very enjoyable to learn with Abu Ashraf and i highly recommend learning with him as he is a great driving instructor!",
            'created_at': '27th Dec 2024',
        },{
            'user': 'Bill Murray-Bruce',
            'rating': 5,
            'comment': "I had the pleasure of taking driving lessons with Abu Ashraf, and I couldn't be happier with the experience. From the very first lesson, Abu Ashraf was incredibly professional, patient, and encouraging. He made sure to explain every concept clearly and provided constructive feedback that helped me improve with each session. What stood out the most was Abu Ashraf ability to create a calm and stress-free learning environment. Their expertise and confidence in teaching made me feel safe and supported, even when I made mistakes. Thanks to Abu Ashraf, I have now passed my driving test, I highly recommend him to anyone looking for a knowledgeable and reliable driving instructor.",
            'created_at': '5th Jun 2024',
        },{
            'user': 'Ben Winter',
            'rating': 5,
            'comment': "Abu was absolutely brilliant in my lessons. He's great at building your confidence and tailors it specifically to the individual. He was always prompt, very reliable and very patient! I cannot recommend him enough and helped me pass first time! Thank you very much Abu for everything.",
            'created_at': '16th May 2023',
        },{
            'user': 'Zara Shah',
            'rating': 5,
            'comment': 'Abu Ashraf is a brilliant instructor he has helped me so much which allowed me to pass first time! He is friendly and explains everything very well so i can fully understand. I recommend him to every learner out there!',
            'created_at': '8th Apr 2024',
        },{
            'user': 'Shristi',
            'rating': 5,
            'comment': 'I had the best driving experience with Abu Ashraf. He provided clear instructions, explained perfectly and instilled confidence in my abilities. He also improved my confidence on the road. He provided an excellent learning experience while making each lesson productive and enjoyable. I highly recommend him for anyone looking to learn to drive efficiently and safely.',
            'created_at': '30th Nov 2023',
        },{
            'user': 'Thomas Jordan Griffiths',
            'rating': 5,
            'comment': "Abu Ashraf - Ash for short taught me from scratch to drive in under 3 months. He has so many ch knowledge of the road and always gave instructions in a calm and friendly manner. I passed 1st time with Ash, and when I first signed up to drive Johnson I thought it would take at least 3 driving test attempts and a lot longer than 3 months! I couldn’t rate Ash any less than 100%!!",
            'created_at': '13th May 2023',
        },{
            'user': 'cait',
            'rating': 5,
            'comment': 'I learnt to drive with Abu Ashraf (Ash) I passed first time with 2 minors after 5 months of lessons. Ash is the only instructor that’s ever simplified driving for me and made it easy to pass. He is really flexible and I will miss our lessons, he always made me feel very at ease.',
            'created_at': '31st May 2023',
        },{
            'user': 'Balkics',
            'rating': 5,
            'comment': 'My son and daughter both passed the driving test on the first attempt. My daughter with zero minors and my son with one. Mr Abu Ashraf is a legend and helped both of them to really learn driving from scratch, be safe drivers and be confident on the road. I highly recommend Mr Ashraf to anyone to come out with flying Colors. Ask him by name folks! Thanks Mr Ashraf and Drivejohnsons. Keep up the good work. Thanks Balki',
            'created_at': '28th Feb 2024',
        },{
            'user': 'Ashraaf Uddin',
            'rating': 5,
            'comment': "I am extremely happy with my experience with learning to drive with Abu Ashraf. I have been learning to drive for a long time and Abu Ashraf has taught me very efficiently. I also worked on all my weaknesses to ensure that I make no mistakes when driving. I also perfected my strengths to ensure that I drive well. Abu Ashraf always answered any questions I had and he made sure that I understand everything he teaches. He demonstrated things to me so I can fully understand the manoeuvres and techniques. He also taught me how to park very well. He gradually and carefully taught me how to park as the days go by. We never rushed anything. By the time my driving test date came, I knew knew I was fully ready. This is because I was fully prepared for it. This is how I passed! I'm very satisfied. I recommend Abu Ashraf to be anyone's instructor.",
            'created_at': '29th Apr 2024',
        },{
            'user': 'Elisabeth Barrow',
            'rating': 5,
            'comment': "Massive thanks to Abu Ashraf. With his patience and passion for his students helped me pass my driving test, the 1st time. I would 100% recommend Abu if you want someone that goes the extra mile for great results.",
            'created_at': '16th Oct 2023',
        },
    ]
    
    # Dynamic reviews from the database
    dynamic_reviews = Review.objects.all().order_by('-created_at')

    # Merge static and dynamic reviews
    combined_reviews = list(chain(static_reviews, dynamic_reviews))

    return render(request, 'reviews.html', {
        'reviews': combined_reviews
    })



# Signup view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')  # Redirect to the login page after successful signup

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('abu')  # Redirect to the 'abu' view after login
            else:
                # If user authentication fails (wrong username or password)
                messages.error(request, "Invalid username or password.")
        else:
            # If form is not valid (for other reasons)
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    # Clear messages related to non-login actions (e.g., review errors)
    if 'review' in request.GET:  # Only clear messages if it's a 'review' related page
        messages.get_messages(request).used = True  # Clears out old messages
        
    return render(request, 'registration/login.html', {'form': form})


# Custom login view
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('abu')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'registration/login.html')


# View to display all reviews
def reviews(request):
    all_reviews = Review.objects.all().order_by('-created_at')  # Sort reviews by created_at in descending order
    return render(request, 'reviews.html', {'reviews': all_reviews})

# views.py
@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('reviews')  # Redirect to reviews page after submission
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'form': form})


# Leave review view for rendering the form
@login_required
def leave_review(request):
    form = ReviewForm()
    return render(request, 'leave_review.html', {'form': form})


@login_required  # Ensure the user is logged in before accessing the profile page
def profile_view(request):
    # The logged-in user's data will be available in 'request.user'
    return render(request, 'profile.html', {'user': request.user})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
        messages.success(request, 'Your review has been deleted successfully!')
    else:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    return redirect('reviews')  # Redirect to reviews page after deletion



# Review list view using class-based view
class ReviewListView(ListView):
    model = Review
    template_name = 'reviews.html'
    context_object_name = 'reviews'


# Submit review view using class-based view
class SubmitReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['comment', 'rating']
    template_name = 'submit_review.html'
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your review has been submitted!")
        return super().form_valid(form)


