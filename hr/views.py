from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from hr.models import JobPost , CandidateApplications , SelectCandidateJob
from hr.models import Hr
from django.contrib.auth import authenticate

@login_required
def hrHome(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if Hr.objects.filter(user=user).exists():
            jobposts = JobPost.objects.filter(user=request.user)
            return render(request,'hr/hrdash.html',{'jobposts':jobposts})
    else:
        return redirect("/dash")
    

@login_required
def hrCandidateDetails(request,id):
    if JobPost.objects.filter(id=id).exists():
        jobpost = JobPost.objects.get(id=id)
        jobapplys = CandidateApplications.objects.filter(job=jobpost)
        # print(jobapplys)
        selectedCandidate = SelectCandidateJob.objects.filter(job=jobpost)
        print(selectedCandidate)
        return render(request,'hr/candidate.html',{'jobapplys':jobapplys,'jobpost':jobpost,'selectedCandidate':selectedCandidate})
    else:
        return render('hrdash') 

@login_required
def postJobs(request):
    if request.method == 'POST':
        job_title = request.POST.get('job-title')
        address = request.POST.get('address')
        company_name = request.POST.get('company-name')
        salary_low = request.POST.get('salary-low')
        salary_high = request.POST.get('salary-high')
        last_date  = request.POST.get('last-date')

        jobpost = JobPost(user=request.user,title=job_title,address=address,companyName=company_name,salaryLow=salary_low,salaryHigh=salary_high,lastDateToApply=last_date)
        jobpost.save()
        msg = "Job Upload Done.."
        return render(request,'hr/postjob.html',{'msg':msg})
    return render(request,'hr/postjob.html')

def acceptApplication(request):
    if request.method == 'POST':
        candidateid = request.POST.get('candidateid')
        jobpostid = request.POST.get('jobpostid') 
        candidate = CandidateApplications.objects.get(id=candidateid) 
        candidate.status = 'accepted'  # Modify the status field
        candidate.save()
        jobpost = JobPost.objects.get(id=jobpostid)
        if SelectCandidateJob.objects.filter(candidate=candidate).exists()==False:
            SelectCandidateJob(job=jobpost,candidate=candidate).save()
        return redirect('/candidatedetails/'+str(jobpostid)+"/")
    return redirect('hrdash')