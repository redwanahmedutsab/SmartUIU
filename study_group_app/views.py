from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Group, GroupMember, Message


@login_required(login_url='/login')
def home(request):
    created_groups = Group.objects.filter(creator=request.user)
    member_groups = Group.objects.filter(group_members__user=request.user)
    all_groups = created_groups | member_groups
    all_groups = all_groups.distinct()
    return render(request, 'study_group/study_group.html', {'groups': all_groups})


@login_required(login_url='/login')
def study_group_create_group_view(request):
    current_user = request.user
    users = User.objects.exclude(id=current_user.id)

    if request.method == 'POST':
        group_name = request.POST.get('name')
        group_description = request.POST.get('description')
        group_photo = request.FILES.get('photo')
        member_ids = request.POST.getlist('members')

        group = Group.objects.create(
            name=group_name,
            description=group_description,
            creator=current_user,
            image=group_photo
        )

        GroupMember.objects.create(group=group, user=current_user, role='admin')

        for member_id in member_ids:
            member = User.objects.get(id=member_id)
            GroupMember.objects.create(group=group, user=member)

        return redirect('study_group')

    return render(request, 'study_group/study_group_create_group.html', {'users': users})


# @login_required(login_url='/login')
# def study_group_chat_view(request, id):
#     group = get_object_or_404(Group, id=id)
#     updated_messages = Message.objects.filter(group=group).order_by('timestamp')
#     current_group = get_object_or_404(Group, id=id)
#
#     if request.method == 'POST':
#         message_content = request.POST.get('message')
#         message_file = request.FILES.get('file')
#
#         # Check if content exists before creating the message
#         if message_content:
#             # Create the new message
#             message = Message.objects.create(
#                 content=message_content,
#                 file=message_file,  # This can be None if no file is uploaded
#                 sender=request.user,
#                 group=group
#             )
#
#             # After the new message is posted, requery updated messages
#             updated_messages = Message.objects.filter(group=group).order_by('timestamp')
#
#             # Prepare the message list
#             message_list = [
#                 {
#                     'sender': msg.sender.get_full_name(),
#                     'username': msg.sender.username,
#                     'content': msg.content,
#                     'file_url': msg.file.url if msg.file else None,
#                     'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#                     'is_mine': msg.sender == request.user,
#                 }
#                 for msg in updated_messages
#             ]
#
#             return JsonResponse({'success': True, 'messages': message_list})
#
#         return JsonResponse({'success': False, 'error': 'Message content cannot be empty.'})
#
#     # Fetch user’s created groups and groups they are members of
#     created_groups = Group.objects.filter(creator=request.user)
#     member_groups = Group.objects.filter(group_members__user=request.user)
#     all_groups = created_groups | member_groups
#     all_groups = all_groups.distinct()
#
#     # Prepare message list for the GET request
#     message_list = [
#         {
#             'sender': message.sender.get_full_name(),
#             'username': message.sender.username,
#             'content': message.content,
#             'file_url': message.file.url if message.file else None,
#             'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#             'is_mine': message.sender == request.user,
#         }
#         for message in updated_messages
#     ]
#
#     return render(request, 'study_group/study_group_chat.html',
#                   {'group': group, 'messages': message_list, 'all_groups': all_groups, 'current_group': current_group})

@login_required(login_url='/login')
def study_group_chat_view(request, id):
    group = get_object_or_404(Group, id=id)
    updated_messages = Message.objects.filter(group=group).order_by('timestamp')
    current_group = get_object_or_404(Group, id=id)

    # Function to check if it's an AJAX request
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'GET' and is_ajax:  # Check if it's an AJAX GET request
        # Prepare the message list for the AJAX response
        message_list = [
            {
                'sender': message.sender.get_full_name(),
                'username': message.sender.username,
                'content': message.content,
                'file_url': message.file.url if message.file else None,
                'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'is_mine': message.sender == request.user,
            }
            for message in updated_messages
        ]
        return JsonResponse({'success': True, 'messages': message_list})

    elif request.method == 'POST' and is_ajax:  # Check if it's an AJAX POST request
        message_content = request.POST.get('message')
        message_file = request.FILES.get('file')

        # Check if content exists before creating the message
        if message_content:
            # Create the new message
            message = Message.objects.create(
                content=message_content,
                file=message_file,  # This can be None if no file is uploaded
                sender=request.user,
                group=group
            )

            # After the new message is posted, requery updated messages
            updated_messages = Message.objects.filter(group=group).order_by('timestamp')

            # Prepare the message list
            message_list = [
                {
                    'sender': msg.sender.get_full_name(),
                    'username': msg.sender.username,
                    'content': msg.content,
                    'file_url': msg.file.url if msg.file else None,
                    'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'is_mine': msg.sender == request.user,
                }
                for msg in updated_messages
            ]

            return JsonResponse({'success': True, 'messages': message_list})

        return JsonResponse({'success': False, 'error': 'Message content cannot be empty.'})

    # Fetch user’s created groups and groups they are members of
    created_groups = Group.objects.filter(creator=request.user)
    member_groups = Group.objects.filter(group_members__user=request.user)
    all_groups = created_groups | member_groups
    all_groups = all_groups.distinct()

    # Prepare message list for the GET request (non-AJAX)
    message_list = [
        {
            'sender': message.sender.get_full_name(),
            'username': message.sender.username,
            'content': message.content,
            'file_url': message.file.url if message.file else None,
            'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'is_mine': message.sender == request.user,
        }
        for message in updated_messages
    ]

    # For non-AJAX requests, render the HTML template
    return render(request, 'study_group/study_group_chat.html',
                  {'group': group, 'messages': message_list, 'all_groups': all_groups, 'current_group': current_group})


@login_required(login_url='/login')
def edit_members(request, id):
    members = GroupMember.objects.filter(group_id=id)
    member_ids = members.values_list('user_id', flat=True)
    users = User.objects.exclude(id__in=member_ids)

    if request.method == 'POST':
        current_members = request.POST.getlist('members')
        removed_members = request.POST.getlist('removed_members')

        for member_id in current_members:
            if not GroupMember.objects.filter(group_id=id, user_id=member_id).exists():
                print(member_id)
                GroupMember.objects.create(group_id=id, user_id=member_id)

        for member_id in removed_members:
            GroupMember.objects.filter(group_id=id, user_id=member_id).delete()

        return redirect('edit_members', id)
    return render(request, 'study_group/add_member.html', {'members': members, 'users': users})


@login_required(login_url='/login')
def delete_group_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.creator == request.user:
        group.delete()

    return redirect('study_group')


@login_required(login_url='/login')
def update_group_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if the user is an admin of the group
    if not group.group_members.filter(user=request.user, role='admin').exists():
        return render(request, 'study_group/study_group.html',
                      {'message': 'You do not have permission to update this group.'})

    if request.method == 'POST':
        group.name = request.POST.get('group_name', group.name)  # Update group name
        group.description = request.POST.get('group_description', group.description)  # Update group description

        # Handle image upload
        if request.FILES.get('image'):
            group.image = request.FILES['image']

        group.save()  # Save the updated group details
        return redirect('study_group')  # Redirect to the available groups page

    return render(request, 'study_group/study_group.html', {'group': group})
