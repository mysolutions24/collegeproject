from fileinput import filename
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect, reverse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.template import context,loader
from .models import Skill, Academic, Referee, Profile, User, Skill, Cv, Experiance, Links, Hobbies, Language, ECA, Contact
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
import pdfkit
from django.core.mail import send_mail
from backend import settings
# pdf generatior
from django.http import HttpResponse
from django.views.generic import View
from core import models
from .process import html_to_pdf 
from django.template.loader import render_to_string


def index(request):
    return render(request, 'core/home.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email  = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact.objects.create(
                c_name=name, c_email=email, c_subject=subject, c_message=message)
        contact.save()

    return render(request, 'core/success.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    return render(request, 'core/login.html')


@login_required
def dashboard(request):
    user_id = request.user.id

    try:
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]
        print('Cv ID is', cv_id)
        print('Data type', type(cv_id))
        if isinstance(cv_id, int):
            context = {'status': 'there_is_cv'}
            return render(request, 'core/dashboard.html', context)
    except Exception as e:
        context = {'status': 'no_cv'}
        return render(request, 'core/dashboard.html', context)


def createCv(request):
    user_id = request.user.id

    try:
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        profile_id = Profile.objects.filter(
            cv_id=cv_id).values_list('id', flat=True)
        profile_id = list(profile_id)
        profile_id = profile_id[0]

        if isinstance(profile_id, int):
            context = {'status': 'there_is_profile'}
            return render(request, 'core/create_cv.html', context)
    except Exception as e:
        context = {'status': 'no_profile'}
        return render(request, 'core/create_cv.html', context)



def saveExperiance(request):
    if request.method == 'POST':
        company = request.POST.getlist('company[]')
        role = request.POST.getlist('role[]')
        duration = request.POST.getlist('duration[]')
        city = request.POST.getlist('city[]')
        bio = request.POST.getlist('bio[]')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if (len(company) == 1):
            x = Experiance(e_company=company[0], e_role=role[0],
                           e_duration=duration[0], e_city=city[0], e_bio=bio[0], cv_id=cv_id)
            x.save()
            return JsonResponse({'status': 1})
        else:
            for a, b, c, d, e in zip(company, role, duration, city, bio):
                x = Experiance(e_company=a, e_role=b, e_duration=c,
                               e_city=d, e_bio=e, cv_id=cv_id)
                x.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


def saveEducation(request):
    if request.method == 'POST':
        name = request.POST.getlist('name[]')
        course = request.POST.getlist('course[]')
        year = request.POST.getlist('year[]')
        award = request.POST.getlist('award[]')
        mark = request.POST.getlist('mark[]')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if (len(name) == 1):
            a = Academic(a_institution=name[0], a_year=year[0], a_award=award[0],
                         a_course=course[0], a_mark=mark[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status': 1})
        else:
            for x, y, z, o, p in zip(name, year, award, course, mark):
                a = Academic(a_institution=x, a_year=y, a_award=z,
                             a_course=o, a_mark=p, cv_id=cv_id)
                a.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


def saveReferee(request):
    if request.method == 'POST':
        name = request.POST.getlist('name[]')
        phone = request.POST.getlist('phone[]')
        email = request.POST.getlist('email[]')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if (len(name) == 1):
            a = Referee(r_name=name[0], r_email=email[0],
                        r_phone=phone[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status': 1})
        else:
            for x, y, z in zip(name, phone, email):
                a = Referee(r_name=x, r_phone=y, r_email=z, cv_id=cv_id)
                a.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


def saveLink(request):
    if request.method == 'POST':
        link_name = request.POST.getlist('link_name[]')
        link = request.POST.getlist('link[]')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if (len(link_name) == 1):
            a = Links(link_name=link_name[0], link=link[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status': 1})
        else:
            for x, y in zip(link_name, link):
                a = Links(link_name=x, link=y, cv_id=cv_id)
                a.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})

def saveSkill(request):
    if request.method == 'POST':
        user_id = request.user.id

        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        s_name = request.POST.getlist('s_name[]')
        s_level = request.POST.getlist('s_level[]')

        if (len(s_name) == 1):
            a = Skill(s_name=s_name[0], s_level=s_level[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status': 1})
        else:
            for x, y in zip(s_level, s_name):
                a = Skill(s_level=x, s_name=y, cv_id=cv_id)
                a.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})



def saveHobby(request):
    if request.method == 'POST':

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        hobby_name = request.POST.getlist('hobby_name[]')


        if (len(hobby_name) == 1):
            a = Hobbies(hobby_name=hobby_name[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status': 1})
        else:
            for x in zip(hobby_name):
                a = Hobbies(hobby_name=x, cv_id=cv_id)
                a.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


def saveLang(request):
    if request.method == 'POST':
        lang_name = request.POST.getlist('lang_name[]')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if (len(lang_name) == 1):
            a = Language(lang_name=lang_name[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status': 1})
        else:
            for x in zip(lang_name):
                a = Language(lang_name=x, cv_id=cv_id)
                a.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


def saveEca(request):
    if request.method == 'POST':
        eca_name = request.POST.getlist('eca_name[]')
        des = request.POST.getlist('des[]')

        user_id = request.user.id
        cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
        cv_id = list(cv_id)
        cv_id = cv_id[0]

        if (len(eca_name) == 1):
            a = ECA(eca_name=eca_name[0], eca_des=des[0], cv_id=cv_id)
            a.save()
            return JsonResponse({'status': 1})
        else:
            for x, y in zip(eca_name, des):
                a = ECA(eca_name=x, eca_des=y, cv_id=cv_id)
                a.save()
            return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


def uploadProfile(request):
    fname = request.POST.get('fname')
    mname = request.POST.get('mname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    gender = request.POST.get('gender')
    bio = request.POST.get('bio')
    dob = request.POST.get('dob')
    occupation = request.POST.get('occupation')
    country = request.POST.get('country')
    region = request.POST.get('region')
    city = request.POST.get('city')
    file = request.FILES.get('file')
    user_id = request.user.id

    Cv.objects.create(user_id=user_id)

    cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
    cv_id = list(cv_id)
    cv_id = cv_id[0]
    print('Cv ID is', cv_id)

    p = Profile(fname=fname, mname=mname, lname=lname, email=email, bio=bio, dob=dob, gender=gender,
                occupation=occupation, country=country, region=region, city=city, avator=file, phone=phone, cv_id=cv_id)
    p.save()

    return JsonResponse({'status': 1})


def updateref(request):
    id = request.POST.get('id')
    r_name = request.POST.get('r_name')
    r_email = request.POST.get('r_email')
    r_phone = request.POST.get('r_phone')

    Referee.objects.filter(id=id).update(r_name=r_name, r_email=r_email, r_phone=r_phone)

    return JsonResponse({'status': 1})



def updateeca(request):
    id = request.POST.get('id')
    eca_name = request.POST.get('eca_name')
    eca_des = request.POST.get('eca_des')

    ECA.objects.filter(id=id).update(eca_name=eca_name, eca_des=eca_des)

    return JsonResponse({'status': 1})



def updatelang(request):
    id = request.POST.get('id')
    lang_name = request.POST.get('lang_name')

    Language.objects.filter(id=id).update(lang_name=lang_name)

    return JsonResponse({'status': 1})



def updatehobby(request):
    id = request.POST.get('id')
    hobby_name = request.POST.get('hobby_name')

    Hobbies.objects.filter(id=id).update(hobby_name=hobby_name)

    return JsonResponse({'status': 1})




def updatelink(request):
    id = request.POST.get('id')
    link_name = request.POST.get('link_name')
    link = request.POST.get('link')

    Links.objects.filter(id=id).update(link_name=link_name, link=link)

    return JsonResponse({'status': 1})


def updateskill(request):
    id = request.POST.get('id')
    s_name = request.POST.get('s_name')
    s_level = request.POST.get('s_level')

    Skill.objects.filter(id=id).update(s_name=s_name, s_level=s_level)

    return JsonResponse({'status': 1})


def updateexp(request):
    id = request.POST.get('id')
    company = request.POST.get('company')
    role = request.POST.get('role')
    duration = request.POST.get('duration')
    city = request.POST.get('city')
    bio = request.POST.get('bio')

    Experiance.objects.filter(id=id).update(
        e_company=company, e_role=role, e_duration=duration, e_city=city, e_bio=bio)

    return JsonResponse({'status': 1})


def updateAcademic(request):
    id = request.POST.get('id')
    institution = request.POST.get('institution')
    year = request.POST.get('year')
    award = request.POST.get('award')
    course = request.POST.get('course')
    mark = request.POST.get('mark')

    Academic.objects.filter(id=id).update(
        a_institution=institution, a_year=year, a_award=award, a_course=course, a_mark=mark)

    return JsonResponse({'status': 1})


def updateProfile(request):
    id = request.POST.get('id')
    fname = request.POST.get('fname')
    mname = request.POST.get('mname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    gender = request.POST.get('gender')
    bio = request.POST.get('bio')
    dob = request.POST.get('dob')
    occupation = request.POST.get('occupation')
    country = request.POST.get('country')
    region = request.POST.get('region')
    city = request.POST.get('city')
    file = request.FILES.get('file')

    user_id = request.user.id
    cv_id = Cv.objects.filter(user_id=user_id).values_list('id', flat=True)
    cv_id = list(cv_id)
    cv_id = cv_id[0]

    Profile.objects.filter(cv_id=id).update(fname=fname, mname=mname, lname=lname, email=email, bio=bio, dob=dob, gender=gender,
                                            occupation=occupation, country=country, region=region, city=city, avator=file, phone=phone, cv_id=cv_id)

    return JsonResponse({'status': 1})


def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)

        check_user = User.objects.filter(username=username).count()
        check_email = User.objects.filter(email=email).count()

        if (check_user > 0):
            messages.error(request, 'Username is already taken')
            return redirect('reg-form')
        elif (check_email > 0):
            messages.error(request, 'Email is already taken')
            return redirect('reg-form')
        else:
            myuser = User.objects.create(
                username=username, email=email, password=password)
            myuser.user_name = username

            messages.success(
                request, 'Account created successfully, Please Sign In')

            # WELCOME EMAIL

            subject = "WELCOME TO ONLINE-RESUME BUILDER!"
            message = "Hello " + myuser.user_name + "!\n" + \
                "Thanks For choosing Our Service.\nYou Can Build Your Attractive resume For Free Without any Charges.\n\n\nThank You!\nHave a Great Day!\n\nRegards\nMudassir Ahmed.."
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)
            return redirect('reg-form')
    else:
        return render(request, 'core/register.html')


def editCv(request):
    return render(request, 'core/edit_cv.html')


def fetchProfile(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_profile = Profile.objects.get(cv_id=id)

    user_profile = {
        'fname': user_profile.fname,
        'mname': user_profile.mname,
        'lname': user_profile.lname,
        'email': user_profile.email,
        'phone': user_profile.phone,
        'bio': user_profile.bio,
        'dob': user_profile.dob,
        'country': user_profile.country,
        'region': user_profile.region,
        'occupation': user_profile.occupation,
        'city': user_profile.city

    }
    return JsonResponse(user_profile)


def fetchAcademic(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_education = Academic.objects.get(id=id)

    user_education = {'institution': user_education.a_institution,
                      'year': user_education.a_year,
                      'award': user_education.a_award,
                      'course': user_education.a_course,
                      'mark': user_education.a_mark,

                      }
    return JsonResponse(user_education)


def fetchexp(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_exp = Experiance.objects.get(id=id)

    user_exp = {'company': user_exp.e_company,
                'role': user_exp.e_role,
                'duration': user_exp.e_duration,
                'city': user_exp.e_city,
                'bio': user_exp.e_bio,

                }
    return JsonResponse(user_exp)


def fetchskill(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_skill = Skill.objects.get(id=id)

    user_skill = {
        's_name': user_skill.s_name,
        's_level': user_skill.s_level,

    }
    return JsonResponse(user_skill)


def fetchlink(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_link = Links.objects.get(id=id)

    user_link = {
        'link_name': user_link.link_name,
        'link': user_link.link,

    }
    return JsonResponse(user_link)


def fetchHobby(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_hobby = Hobbies.objects.get(id=id)

    user_hobby = {
        'hobby_name': user_hobby.hobby_name,

    }
    return JsonResponse(user_hobby)


def fetchlang(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_lang = Language.objects.get(id=id)

    user_lang = {
        'lang_name': user_lang.lang_name,

    }
    return JsonResponse(user_lang)


def fetcheca(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_eca = ECA.objects.get(id=id)

    user_eca = {
        'eca_name': user_eca.eca_name,
        'eca_des': user_eca.eca_des,

    }
    return JsonResponse(user_eca)

def fetchref(request):
    id = request.POST.get('id')
    print('Cv ID is', id)

    user_ref = Referee.objects.get(id=id)

    user_ref = {
        'r_name': user_ref.r_name,
        'r_email': user_ref.r_email,
        'r_phone': user_ref.r_phone,

    }
    return JsonResponse(user_ref)



def deleteProfile(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_profile = Profile.objects.get(cv_id=id)
        user_profile.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def deleteAcademic(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_education = Academic.objects.get(id=id)
        user_education.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def deleteExp(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_exp = Experiance.objects.get(id=id)
        user_exp.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def deleteSkill(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_skill = Skill.objects.get(id=id)
        user_skill.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def deleteLink(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_link = Links.objects.get(id=id)
        user_link.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})



def deleteHobby(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_hobby = Hobbies.objects.get(id=id)
        user_hobby.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def deletelang(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_lang = Language.objects.get(id=id)
        user_lang.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})



def deleteeca(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_eca = ECA.objects.get(id=id)
        user_eca.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def deleteref(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print('Cv ID is', id)

        user_ref = Referee.objects.get(id=id)
        user_ref.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})



def educationView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_education = Academic.objects.filter(cv_id=id).all()
    context = {'user_education': user_education}
    return render(request, 'core/education_view.html', context)


def experianceView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_experiance = Experiance.objects.filter(cv_id=id).all()
    context = {'user_experiance': user_experiance}
    return render(request, 'core/exp_view.html', context)


def skillView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_skill = Skill.objects.filter(cv_id=id).all()
    context = {'user_skill': user_skill}
    return render(request, 'core/skill_view.html', context)


def linkView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_link = Links.objects.filter(cv_id=id).all()
    context = {'user_link': user_link}
    return render(request, 'core/link_view.html', context)


def hobbyView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_hobby = Hobbies.objects.filter(cv_id=id).all()
    context = {'user_hobby': user_hobby}
    return render(request, 'core/hobby_view.html', context)


def langView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_lang = Language.objects.filter(cv_id=id).all()
    context = {'user_lang': user_lang}
    return render(request, 'core/lang_view.html', context)

def ecaView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_eca = ECA.objects.filter(cv_id=id).all()
    context = {'user_eca': user_eca}
    return render(request, 'core/eca_view.html', context)


def refView(request):
    id = request.user.cv.id
    print('Cv ID is', id)
    user_ref = Referee.objects.filter(cv_id=id).all()
    context = {'user_ref': user_ref}
    return render(request, 'core/ref_view.html', context)



#Creating a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        data = models.Profile.objects.all().order_by('fname')
        open('core/pdf_template.html', "w").write(render_to_string('core/pdf_template.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('core/pdf_template.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')



def logoutView(request):
    logout(request)
    return redirect('index')


def viewPDF(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template1.html', context)



def viewPDF1(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template1.html', context)

def viewPDF2(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template2.html', context)


def viewPDF3(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template3.html', context)

def viewPDF4(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template4.html', context)


def viewPDF5(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template5.html', context)


def viewPDF6(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template6.html', context)



def viewPDF7(request, id=None):
    user_profile = Profile.objects.filter(cv_id=id)
    user_skill = Skill.objects.filter(cv_id=id).values()
    user_referee = Referee.objects.filter(cv_id=id).values()
    user_education = Academic.objects.filter(cv_id=id).values()
    user_exp = Experiance.objects.filter(cv_id=id).values()
    user_link = Links.objects.filter(cv_id=id).values()
    user_hobby = Hobbies.objects.filter(cv_id=id).values()
    user_lang = Language.objects.filter(cv_id=id).values()
    user_eca = ECA.objects.filter(cv_id=id).values()


    context = {'user_profile': user_profile, 'user_skill': user_skill,
               'user_referee': user_referee, 'user_education': user_education,
               'user_exp':user_exp,'user_link':user_link,'user_hobby':user_hobby,'user_lang':user_lang,
               'user_eca':user_eca}
    
    return render(request, 'core/pdf_template7.html', context)




def selectPDF(request,id=None):
    return render(request,'core/select_template.html')






