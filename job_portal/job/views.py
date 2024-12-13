from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.http import HttpResponse
from .models import *

def home(request):
    return render(request,'homepage.html')

def adminhome(request):
    return render(request,'admin_home.html')

@login_required
def companyhome(request):
    return render(request,'companyhome.html')

@login_required
def userhome(request):
    return render(request,'userhome.html')

def logins(request):
    if request.method=="POST":
        un=request.POST["uname"]
        ps=request.POST["pass"]
        user=authenticate(request,username=un,password=ps)
        if user is not None and user.is_superuser==1:
            return redirect(adminhome)
        elif user is not None and user.is_staff==1:
            print("COMPANY")
            login(request,user)
            request.session['Company_id']=user.id
            print('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////',user.id)

            return redirect(companyhome)
        elif user is not None and user.is_active==1:
            login(request,user)
            request.session['user_id']=user.id
            return redirect(userhome)
        else:
            return HttpResponse("not valid")
    else:
        return render(request,'login.html')


@never_cache
def logouts(request):
    logout(request)
    return redirect(logins)

def add_department(request):
    if request.method=="POST":
        Departmentname=request.POST['dep']
        x=Department.objects.create(departmentname=Departmentname)
        x.save()
        return HttpResponse("<script>alert('Added Successfully !!!');window.location.href='/adminhome';</script>")
    else:
        return render(request,'adddepartment.html')
    
def department_view(request):
    departments = Department.objects.all()
    return render(request, 'department_view.html', {'departments': departments})

def admin_skill(request):
    if request.method=="POST":
        skillname=request.POST['sk']
        x=Skill.objects.create(sk_name=skillname)
        x.save()
        return HttpResponse("<script>alert('Added Successfully !!!');window.location.href='/adminhome';</script>")
    else:
        return render(request,'adminskill.html')

def admin_user_view(request):
    profile=Profile.objects.all()
    return render(request,'admin_user_view.html',{'profile':profile})


def admin_user_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profile.user_id.first_name = request.POST.get('first_name', profile.user_id.first_name)
        profile.user_id.last_name = request.POST.get('last_name', profile.user_id.last_name)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.location = request.POST.get('location', profile.location)
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
        skills_ids = request.POST.getlist('skills')  
        profile.skills.set(skills_ids)  
        profile.user_id.save()
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('admin_user_view')
    skills = Skill.objects.all()
    context = {
        'profile': profile,
        'skills': skills,
        'selected_skills': [skill.id for skill in profile.skills.all()],
    }
    return render(request, 'admin_user_edit.html', context)


def admin_user_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile deleted successfully.')
        return redirect('admin_user_view')

    return render(request, 'delete_profile.html', {'profile': profile})

def admin_skill_view(request):
    if request.method == 'POST' and 'delete' in request.POST:
        skill_id = request.POST.get('delete')
        skill = Skill.objects.get(id=skill_id)
        skill.delete() 
        return redirect('admin_skill_view') 
    ski = Skill.objects.all()
    return render(request, 'admin_skill_view.html', {'x1': ski})

def adminapplic(request):
    applications = Application.objects.all()
    query = request.GET.get('q')
    if query:
        applications = applications.filter(
            user_id__user_id__first_name__icontains=query
        ) | applications.filter(
            job_id__title__icontains=query
        ) | applications.filter(
            job_id__company_id__Company_Name__icontains=query
        ) | applications.filter(
            job_id__department_id__departmentname__icontains=query
        )
    return render(request, 'adminapplic.html', {'applic': applications, 'query': query})

def add_company(request):
    if request.method=="POST":
        uname = request.POST['uname']
        passw = request.POST['passw']
        email = request.POST['email']
        dep = request.POST['dep']
        companyname = request.POST['cname']
        details = request.POST['deta']  
        location = request.POST['loca']
        logoo = request.FILES.get('logo')

        print(f'Department ID////////////////////////////////////////////////////////////////////////////////////: {dep}')


        y = User.objects.create_user(email=email, username=uname, password=passw,user_type='COMPANY',is_staff=True)
        y.save()
        x=Company.objects.create(Company_id=y,Department_id_id=dep,Company_Name=companyname,Details=details,location=location,logo=logoo)
        x.save()
        return HttpResponse("<script>alert('Added Successfully !!!');window.location.href='/login';</script>")
    else:
        departments = Department.objects.all()
        return render(request, 'add_company.html', {'x1': departments})

@login_required
def company_user_view(request):
    comp=request.session.get('Company_id')
    use=Company.objects.get(Company_id=comp)
    return render(request,'company_user_view.html',{'view':use})

def company_view(request):
    query = request.GET.get('q', '')  
    if query:
        companies = Company.objects.filter(
            Q(Company_Name__icontains=query) | Q(location__icontains=query)
        )
    else:
        companies = Company.objects.all()
    return render(request, 'company_view.html', {'companies': companies, 'query': query})

@login_required
def update_company(request, id):
    company = get_object_or_404(Company, id=id)

    if request.method == "POST":
        company.Company_id.username = request.POST['uname']
        company.Company_id.email = request.POST['email']
        company.Company_id.save() 
        company.Department_id_id = request.POST['dep']
        company.Company_Name = request.POST['cname']
        company.Details = request.POST['deta']
        company.location = request.POST['loca']
        
        if request.FILES.get('logo'):
            company.logo = request.FILES['logo']
        
        company.save() 
        return HttpResponse("<script>alert('Updated Successfully !!!');window.location.href='/company_user_view';</script>")
    else:
        departments = Department.objects.all()
        return render(request, 'update_company_id.html', {'company': company, 'departments': departments})


@login_required
def delete_company(request, id):
    company = get_object_or_404(Company, id=id)
    if request.method == "POST":
        company.delete()
        return redirect('company_view')

def user_register(request):
    if request.method == "POST":
        fn = request.POST['fname']
        ln = request.POST['lname']
        em = request.POST['em']
        phon = request.POST['phone']
        loca = request.POST['loca']
        resu = request.FILES.get('resu') 
        un = request.POST['uname']
        ps = request.POST['pass']
        x = User.objects.create_user(first_name=fn, last_name=ln, email=em, username=un, password=ps, user_type='USER', is_active=True)
        x.save()
        z = Profile.objects.create(phone=phon, resume=resu if resu else None, location=loca, user_id=x)
        z.save()
        
        return HttpResponse("<script>alert('Registration Successfully !!!');window.location.href='/login';</script>")
    else:
        return render(request, 'user_registration.html')


@login_required
def user_view(request):
    users=request.session.get('user_id')
    use=Profile.objects.get(user_id_id=users)
    return render(request,'user_view.html',{'view':use})

@login_required
def user_profile(request):
    user_profile, created = Profile.objects.get_or_create(user_id=request.user)
    if request.method == "POST":
        request.session['first_name'] = request.POST.get('first_name', '')
        request.session['location'] = request.POST.get('location', '')
        request.session['selected_skills'] = request.POST.getlist('skills') 
        if 'confirm' in request.POST:
            user_profile.user_id.first_name = request.session.get('first_name', '')
            user_profile.location = request.session.get('location', '')
            selected_skills = request.session.get('selected_skills', [])
            user_profile.skills.set(selected_skills)  
            user_profile.save()
            del request.session['first_name']
            del request.session['location']
            del request.session['selected_skills']

            return redirect(userhome) 
    skills = Skill.objects.all()
    context = {
        'profile': user_profile,
        'skills': skills,
        'first_name': request.session.get('first_name', user_profile.user_id.first_name),
        'location': request.session.get('location', user_profile.location),
        'selected_skills': request.session.get('selected_skills', [skill.id for skill in user_profile.skills.all()]),
    }
    return render(request, 'skill_view.html', context)

@login_required
def user_profilsk(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'user_skill.html', {'x': None, 'error': "User not logged in."})
    x = Profile.objects.filter(user_id=user_id).prefetch_related('skills')  
    return render(request, 'user_skill.html', {'x': x})


@login_required
def remove_skill(request, profile_id, skill_id):
    """
    Removes a specific skill from a profile.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    skill = get_object_or_404(Skill, id=skill_id)
    if skill in profile.skills.all():  
        profile.skills.remove(skill)
        messages.success(request, f"Skill '{skill.sk_name}' removed successfully.")
    else:
        messages.error(request, f"Skill '{skill.sk_name}' is not associated with the profile.")
    return redirect('user_profilsk') 

@login_required
def user_edit(request):
    x = request.session.get('user_id')
    y = Profile.objects.get(user_id_id=x)
    uid = y.user_id_id
    us = User.objects.get(id=uid)
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        p = request.POST['phon']
        loc = request.POST['loc']
        
        if 'resume' in request.FILES:
            y.resume = request.FILES['resume']
        
        y.phone = p
        y.location = loc
        us.first_name = f
        us.last_name = l
        us.email = e
        y.save()
        us.save()
        return redirect(user_view)
    else:
        return render(request, 'user_update.html', {'y': y})

@login_required
def user_delete(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  
    profile = get_object_or_404(Profile, user_id_id=user_id)
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        profile.delete()
        user.delete()    
        request.session.flush()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')  
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
def create_job(request):
    if not request.user.is_staff: 
        return HttpResponse("You do not have permission to create jobs.")
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        closing_date = request.POST['closing_date']
        department_id = request.POST['department']
        skill_id = request.POST['skill']
        department = get_object_or_404(Department, id=department_id)
        skill = get_object_or_404(Skill, id=skill_id)
        company_id = request.session.get('Company_id')
        print('///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////',company_id)
        if not company_id:
            return HttpResponse("Company ID not found in session. Please log in again.")
        try:
            company = Company.objects.get(Company_id=company_id)
        except Company.DoesNotExist:
            return HttpResponse("Company not found. Please check your session data.")        
        job = Job.objects.create(
            title=title,
            description=description,
            location=location,
            closing_date=closing_date,
            department_id=department,
            skill_id=skill,
            company_id=company
        )
        job.save()

        return HttpResponse("<script>alert('Job Created Successfully!');window.location.href='/companyhome';</script>")    
    departments = Department.objects.all()
    skills = Skill.objects.all()
    return render(request, 'create_job.html', {'departments': departments, 'skills': skills})

@login_required
def job_view(request):
    company_id = request.session.get('Company_id')  
    print('Company ID from session:', company_id)
    if not company_id:
        return HttpResponse("Company ID not found in session.")    
    try:
        company = Company.objects.get(Company_id=company_id) 
        print('Retrieved Company:', company)
    except Company.DoesNotExist:
        return HttpResponse("No company found with the given Company ID.")    
    jobs = Job.objects.filter(company_id=company)
    print('Jobs found:', jobs)
    return render(request, 'job_view.html', {'jobs': jobs})

@login_required
def job_list(request):
    query = request.GET.get('q', '')  
    jobs = Job.objects.filter(closing_date__gte=timezone.now())  
    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(location__icontains=query)

    return render(request, 'job_list.html', {'jobs': jobs, 'query': query})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def apply_for_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('login') 
    job = get_object_or_404(Job, id=job_id)
    if job.closing_date < timezone.now():
        return HttpResponse("This job application has already closed.")
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        return HttpResponse("Profile not found. Please complete your profile first.")
    if Application.objects.filter(user_id=profile, job_id=job).exists():
        return HttpResponse("You have already applied to this job.")
    application = Application.objects.create(
        user_id=profile,
        job_id=job,
        company_id=job.company_id,  
        status='applied', 
    )
    application.save()
    return HttpResponse("<script>alert('Application Submitted Successfully!');window.location.href='/userhome';</script>")

@login_required
def update_job(request, job_id):
    if not request.user.is_staff:  
        return HttpResponse("You do not have permission to update jobs.")
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.location = request.POST['location']
        job.closing_date = request.POST['closing_date']
        job.department_id = get_object_or_404(Department, id=request.POST['department'])
        job.skill_id = get_object_or_404(Skill, id=request.POST['skill'])
        job.save()
        return HttpResponse("<script>alert('Job Updated Successfully!');window.location.href='/companyhome';</script>")
    departments = Department.objects.all()
    skills = Skill.objects.all()
    return render(request, 'update_job.html', {'job': job, 'departments': departments, 'skills': skills})

@login_required
def delete_job(request, job_id):
    if not request.user.is_staff:  
        return HttpResponse("You do not have permission to delete jobs.")
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        job.delete()
        return HttpResponse("<script>alert('Job Deleted Successfully!');window.location.href='/companyhome';</script>")

    return render(request, 'delete_job.html', {'job': job})

@login_required
def viewjobapply(request):
    company_id = request.session.get('Company_id')
    if not company_id:
        return HttpResponse("Company ID not found in session. Please log in as a company.")

    try:
        company = Company.objects.get(Company_id=company_id)
    except Company.DoesNotExist:
        return HttpResponse("No company found with the given Company ID.")

    jobs = Job.objects.filter(company_id=company)

    applications = Application.objects.filter(job_id__in=jobs).select_related(
        'job_id', 'job_id__skill_id', 'user_id', 'user_id__user_id'
    )

    query = request.GET.get('q')
    if query:
        applications = applications.filter(
            job_id__title__icontains=query
        ) | applications.filter(
            user_id__user_id__first_name__icontains=query
        ) | applications.filter(
            user_id__user_id__last_name__icontains=query
        ) | applications.filter(
            job_id__skill_id__sk_name__icontains=query
        )

    return render(request, "viewjobapply.html", {"applications": applications, "query": query})


