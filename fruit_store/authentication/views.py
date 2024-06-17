from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from authentication.models import User, Address
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
import re
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password


name_pattern = r'^[A-Za-z]+$'
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}$'

# code for password validation
def validate_password(password):
    # Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character
    if not re.search(r"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}", password):
        return False
    return True


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        mobNo = request.POST.get('mobNo')
        password = request.POST.get('password')
        Cpassword = request.POST.get('Cpassword')

        if ((len(first_name)<2) or (not re.match(name_pattern, first_name)) or (not first_name)):
            messages.error(request, "Please Enter Valid First Name")
            
        elif ((len(lastname)<3) or (not re.match(name_pattern, lastname)) or (not lastname)):
            messages.error(request, "Please Enter Valid Last Name")
            
        elif(len(mobNo) != 10):
            messages.error(request, "Please Enter Valid Mobile No.")
            
        elif (not re.match(email_pattern, email) or email.rfind(".") <= email.index('@')+2):
            messages.error(request, "Please Enter Valid Email Address")
            
        elif(not validate_password(password)):
            messages.error(request, "Please Enter Password in Specified Pattern Only")
            
        elif(password != Cpassword):
            messages.error(request, "Password Not Matched")
        else:
            try:
                if User.objects.filter(username=email).exists():
                    messages.warning(request, "This Email Already Rregistered with us...Please Login and Continue")
                else:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        first_name=first_name,
                        last_name=lastname,
                        password=password,
                        mobNo=mobNo
                    )
                    user.save()
                    messages.success(request, 'Signup Successful..Please login and Enjoy Shopping')
                    return redirect('/authentication/login')
            except Exception as e:
                messages.error(request, "Please Enter Valid Credentials")
                
    return render(request, 'user_auth/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        
        
        if user is None:
            messages.error(request, "Please enter valid Credentials")
        else:
            auth_login(request, user)
            
            if Address.objects.filter(user=user).exists():
                messages.success(request, f"Logged in as {user.first_name}")
                return redirect('/') 
            else:
                messages.success(request, f"Logged in as {user.first_name}")
                return redirect('/authentication/address')
    return render(request, 'user_auth/login.html')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    next_page = request.GET.get('next')
    if next_page:
        return redirect(next_page)
    return redirect('/')



@login_required
def address(request):
    
    if request.method == 'POST':
        try:
            address_type = request.POST['address_type']
            street1 = request.POST['street1']
            street2 = request.POST['street2']
            city = request.POST['city']
            pincode = request.POST['pincode']
            mobile_number = request.POST['mobile_number']
            
            # Check for empty fields
            if not address_type or not street1 or not city or not pincode or not mobile_number:
                raise ValueError("Please fill in all required fields.")
            
            # Save the address if all fields are filled
            Address.objects.create(
                address_type=address_type,
                street1=street1,
                street2=street2,
                city=city,
                pincode=pincode,
                mobile_number=mobile_number,
                user=request.user
            )
            messages.success(request, "Address saved successfully")
            return redirect('/')
        except KeyError as e:
            messages.error(request, f"Missing field: {e.args[0]}")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "An unexpected error occurred. Please try again.")
        
        # Re-render the form with the existing data
        return render(request, 'user_auth/user_address.html', {
            'address_type': request.POST.get('address_type', ''),
            'street1': request.POST.get('street1', ''),
            'street2': request.POST.get('street2', ''),
            'city': request.POST.get('city', ''),
            'pincode': request.POST.get('pincode', ''),
            'mobile_number': request.POST.get('mobile_number', ''),
        })
    else:
        return render(request, 'user_auth/user_address.html', {
            'address_type': '',
            'street1': '',
            'street2': '',
            'city': '',
            'pincode': '',
            'mobile_number': '',
        })

@login_required
def skip_address(request):
    user = request.user
    messages.success(request, f"Logged in as {user.first_name}")
    return redirect('/')  

def forgot_password(request):
    return render(request, 'user_auth/forgot_password.html')

# *************************************************Editing Profile views section start*************************************************#

@login_required
def profileEdit(request, uid):
    user = get_object_or_404(User, id=uid)
    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        address = None
    
    if request.method == "GET":
        context = {"user": user, "address": address}
        return render(request, "user_auth/profile.html", context)
    
    elif request.method == "POST":
        if 'old_password' in request.POST and 'new_password' in request.POST and 'confirm_password' in request.POST:
            # Handle password change form submission
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validate old password
            if not user.check_password(old_password):
                messages.error(request, 'Your old password is incorrect.')
                return redirect('profileEdit', uid=uid)
            
            # Validate new password and confirm password
            if new_password != confirm_password:
                messages.error(request, 'New password and confirm password do not match.')
                return redirect('profileEdit', uid=uid)
            elif old_password == new_password:
                messages.error(request, 'New password must be different from the old password.')
                return redirect('profileEdit', uid=uid)
            
            # Set the new password
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Update session with new password hash
            messages.success(request, 'Your password was changed successfully..!')
            return redirect('profileEdit', uid=uid)
        
        elif 'first_name' in request.POST or 'last_name' in request.POST or 'email' in request.POST or 'mobNo' in request.POST or 'profile_img' in request.POST:
            # Handle profile update form submission
            fname = request.POST.get('first_name', '')
            lname = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            mobNo = request.POST.get('mobNo', '')
            profile_img = request.FILES.get('profile_img')
            
            if len(fname) < 2 or not re.match(name_pattern, fname):
                messages.error(request, "Please enter valid First Name")
            elif len(lname) < 3 or not re.match(name_pattern, lname):
                messages.error(request, "Please enter valid Last Name")
            elif len(mobNo) != 10:
                messages.error(request, "Please enter a valid 10-digit Mobile No.")
            elif not re.match(email_pattern, email) or email.rfind(".") <= email.index('@') + 2:
                messages.error(request, "Please enter valid Email Address")
            else:
                # Update user profile
                user.email = email
                user.first_name = fname
                user.last_name = lname
                user.mobNo = mobNo  
                if profile_img:
                    user.profile_img = profile_img
                user.save()
                messages.success(request, "Profile Updated Successfully!")
            
        elif 'address_type' in request.POST or 'street1' in request.POST or 'street2' in request.POST or 'city' in request.POST or 'pincode' in request.POST:
            # Handle address update form submission
            address_type = request.POST.get('address_type', '')
            street1 = request.POST.get('street1', '')
            street2 = request.POST.get('street2', '')
            city = request.POST.get('city', '')
            pincode = request.POST.get('pincode', '')
            
            # Update or create address
            try:
                if address:
                    # Update existing address
                    address.address_type = address_type
                    address.street1 = street1
                    address.street2 = street2
                    address.city = city
                    address.pincode = pincode
                    address.save()
                else:
                    # Create new address
                    Address.objects.create(
                        user=user,
                        address_type=address_type,
                        street1=street1,
                        street2=street2,
                        city=city,
                        pincode=pincode,
                        mobile_number=user.mobNo
                    )
                messages.success(request, "Address Updated Successfully!")
            except Exception as e:
                messages.error(request, f"Something went wrong... Try again! {e}")

    # If the execution reaches here, it means no redirection occurred, so we render the profile page.
    return redirect('profileEdit', uid=uid)


@login_required
def delete_account(request):
    if request.method == 'POST':
        try:
            request.user.delete()
            auth_logout(request)
            return JsonResponse({'success': True, 'message': 'Account deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


# *************************************************Editing Profile views section start*************************************************#


def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password is incorrect.')
            return redirect('password_change')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('password_change')

        if old_password == new_password:
            messages.error(request, 'New password must be different from the old password.')
            return redirect('password_change')

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('profile')  
    else:
        return render(request, 'user_auth/profile.html')