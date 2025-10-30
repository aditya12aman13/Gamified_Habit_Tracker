from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitEntry
from django.utils import timezone
from django.contrib import messages

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user).prefetch_related('entries')
    today = timezone.localdate()
    return render(request, "home.html", {"habits": habits, "today": today})

@login_required
def create_habit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description", "")
        if title:
            Habit.objects.create(user=request.user, title=title, description=desc)
            messages.success(request, "Habit created.")
            return redirect("dashboard")
    return render(request, "create_habit.html")

@login_required
def toggle_done(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.localdate()
    entry, created = HabitEntry.objects.get_or_create(habit=habit, date=today)
    entry.done = not entry.done
    if entry.done:
        entry.earned_points = 10  # simple rule: 10 points per day
        habit.points += entry.earned_points
    else:
        # revert points if toggled off
        habit.points = max(0, habit.points - entry.earned_points)
        entry.earned_points = 0
    entry.save()
    habit.save()
    return redirect("dashboard")
