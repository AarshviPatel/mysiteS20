from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Topic, Course
from .forms import *

def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-price')[:5]
    return render(request, 'myapp/index.html', {'top_list': top_list,'course_list':course_list})

'''def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-price')[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of topics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        para = '<p>'+ str(topic.id) + ': ' + str(topic) + '</p>'
        response.write(para)
    for course in course_list:
        if course.for_everyone:
            para = '<p>' + str(course) + ': This Course is For Everyone!' + '</p>'
        else:
            para = '<p>' + str(course) + ': This Course is Not For Everyone!' + '</p>'
        response.write(para)
    return response'''

def about(request):
    data="This is an E-Learning WebApp! Search our Topics to find all available Courses."
    return render(request, 'myapp/about.html',{'data':data})

'''def detail(request,top_no):
    response=HttpResponse()
    topic=Topic.objects.filter(id=top_no).values('name','category')
    category=topic[0].get('category')
    heading1='<p><h2>' + 'Category: ' +category+ '</h2></p>'
    response.write(heading1)
    heading2 = '<h1>' +'List of Courses :: ' + '</h1>'
    response.write(heading2)
    topic_name = topic[0].get('name')
    all_courses=Course.objects.filter(topic__name=topic_name)
    for i in all_courses:
        para = '<p>' + str(i) + '</p>'
        response.write(para)
    return response
'''
def detail(request,top_no):
    response=HttpResponse()
    topic= get_object_or_404(Topic,pk=top_no)
    all_courses = Course.objects.filter(topic__name=topic.name)
    return render(request, 'myapp/detail.html', {'topic': topic, 'all_courses':all_courses})

def courses(request):
    courlist=Course.objects.all().order_by('id')
    return render(request,'myapp/courses.html',{'courlist':courlist})

def place_order(request):
    msg=''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                if(order.course.price>150.00):
                    Course.discount(order.course)
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})

def coursedetail(request,cour_id):
    courdetail = Course.objects.get(pk=cour_id)
    if request.method=='POST':
        form=InterestForm((request.POST))
        if form.is_valid():
            if form['interested']==1:
                courdetail.interested=courdetail.interested+1
                courdetail.save()
        return redirect('myapp:index')
    else:
        form = InterestForm()
        return render(request,'myapp/coursedetail.html',{'form':form,'courdetail':courdetail})