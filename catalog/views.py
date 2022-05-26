from tkinter.tix import Tree
from unicodedata import category
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import IssueBooksForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['catgory']
        publisher = request.POST['publisher']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category, publisher=publisher)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    return render(request, "add_book.html")

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_students.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_member(request):
    members = Member.objects.all()
    return render(request, "view_members.html", {'members':members})

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = forms.IssueBooksForm()
    if request.method == "POST":
        form = forms.IssueBooksForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.member_id = request.POST['name2']
            obj.isbn = request.POST['isdbn2']
            obj.save()
            alert = True
            return render(request, "issue_books.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d = days.days
        fine = 0
        if d>14:
            day = d-14
            fine = day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        members = list(models.Member.objects.filter(user=i.member_id))
        i = 0
        for l in books:
            t = (members[i].user,
            members[i].member_id,
            books[i].isbn,
            issuedBooks[0].issued_date,
            issuedBooks[0].expiry_date,
            fine)
            i = i+1
            details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/admin_login')
def member_issued_books(request):
    member = Member.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(member_id=member[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.name,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d = days.days
        fine = 0
        if d<15:
            day = d-14
            fine = d*5
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request, 'student_issued_books.html',{'li1':li1, 'li2':li2})

@login_required(login_url = '/admin_login')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url = '/admin_login')
def edit_profile(request):
    member = Member.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        roll_no = request.POST['roll_no']

        member.user.email = email
        member.phone = phone
        member.roll_no = roll_no
        member.user.save()
        member.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert})
    return render(request, "edit_profile.html")

def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

def delete_member(request, myid):
    member = Member.objects.filter(id=myid)
    member.delete()
    return redirect("/view_member")

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                pass
        except:
            pass
    return render(request, "change_password.html")

@csrf_exempt 
def member_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        roll_on = request.POST['roll_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmach = True
            return render(request, "member_registration.html", {'passnotmach':passnotmach})
        
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        member = Member.objects.create(user=user, phone=phone, roll_on=roll_on, image=image)
        user.save()
        member.save()
        alert = True
        return render(request, "member_registration.html", {'alert':alert})
    return render(request, "member_registration.html")

def member_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You aren't Member")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "member_login.html", {'alert':alert})
    return render(request, "member_login.html")

def admin_login(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You aren't Admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")