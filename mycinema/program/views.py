from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

import pytz
import tzlocal
import datetime
import calendar

from program.models import Show, Ticket


@login_required(login_url='/accounts/login')
def index(request):
    context = {
        'program_days': dict()
    }

    current_day_setup = False

    for i in range(7):
        program_day = datetime.datetime.today() + datetime.timedelta(days=i)
        week_human_day = calendar.day_name[program_day.weekday()]
        week_day = '{:02d}'.format(program_day.day)
        current_month = calendar.month_name[program_day.month]

        program_day_beautify = '{}, {} {}'.format(week_human_day, week_day, current_month)

        if current_day_setup is False:
            current_day_setup = True
            context['program_days'][
                program_day_beautify.replace(' ', '_').replace(',', '_')] = {
                'date': program_day,
                'date_beautify': program_day_beautify,
                'current_day': True,
                'movies': dict()
            }
        else:
            context['program_days'][
                program_day_beautify.replace(' ', '_').replace(',', '_')] = {
                'date': program_day,
                'date_beautify': program_day_beautify,
                'movies': dict()}

    for program_day in context.get('program_days'):
        date = context['program_days'][program_day]['date']

        # check for movies
        query_movies = Show.objects.filter(is_published=True, movie_id__is_published=True).order_by('hour_begin')

        for show in query_movies.iterator():
            show_day = show.date
            if date.day == show_day.day and date.month == show_day.month and date.year == show_day.year:
                show_name = show.movie_id.name
                if not context['program_days'][program_day]['movies'].get(show_name):
                    context['program_days'][program_day]['movies'][show_name] = {
                        'id': show.movie_id.id,
                        'price': show.movie_id.price,
                        'hours_rooms': dict()
                    }

                context['program_days'][program_day]['movies'][show_name]['hours_rooms'][
                    '{:02d}:{:02d}'.format(show.hour_begin.hour, show.hour_begin.minute)] = {
                    'show_id': show.id,
                    'room_name': show.room_id.name,
                    'room_rows': show.room_id.row_sits,
                    'room_cols': show.room_id.column_sits,
                    'date': show.date
                }

    return render(request, 'program/program.html', context)


@login_required(login_url='/accounts/login')
def booking(request):
    if request.method == 'POST':
        show_id = request.POST['show_id']
        movie = request.POST['movie']
        room = request.POST['room']
        date = request.POST['date']
        hour = request.POST['hour']
        price = request.POST['price']
        rows = int(request.POST['rows'])
        cols = int(request.POST['cols'])

        date = date.replace('p.m.', 'PM')
        date = date.replace('a.m.', 'AM')

        try:
            date = datetime.datetime.strptime(date, "%B %d, %Y, %I:%M %p")
            date = date.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            try:
                date = datetime.datetime.strptime(date, "%B %d, %Y, %I %p")
                date = date.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                pass

        query_show = Show.objects.filter(movie_id__name=movie, room_id__name=room, hour_begin__icontains=hour,
                                         date__icontains=date, movie_id__price=price, room_id__row_sits=rows,
                                         room_id__column_sits=cols)
        if query_show.count():
            seats = list()
            tickets = list()
            show_data = query_show.last()
            query_tickets = Ticket.objects.filter(show_id=show_data.id)

            for ticket in query_tickets:
                tickets.append((ticket.row_num, ticket.col_num))

            for i in range(rows):
                for j in range(rows):
                    if (i, j) in tickets:
                        seats.append((i + 1, j + 1, 'booked'))
                    else:
                        seats.append((i + 1, j + 1, 'free'))

            seats = [seats[i:i + rows] for i in range(0, len(seats), rows)]

            context = {
                'show_id': show_id,
                'movie': movie,
                'room': room,
                'date': date,
                'hour': hour,
                'price': price,
                'rows': [i + 1 for i in range(rows)],
                'cols': [i + 1 for i in range(cols)],
                'seats': seats
            }
            return render(request, 'program/booking.html', context)
        else:
            return redirect('program')
    else:
        return redirect('program')


@login_required(login_url='/accounts/login')
def book_ticket(request):
    if request.method == 'POST':
        show_id = request.POST['show_id']
        row = int(request.POST['row']) - 1
        col = int(request.POST['col']) - 1
        ticket_query = Ticket.objects.filter(show_id=show_id, row_num=row, col_num=col)
        if ticket_query.count() > 0:
            return redirect('program')
        else:
            user = User.objects.get(id=request.user.id)
            show = Show.objects.get(id=show_id)
            ticket = Ticket(user_id=user, show_id=show, row_num=row, col_num=col, is_paid=True, is_valid=True)
            ticket.save()
            # render page
            show_id = request.POST['show_id']
            movie = request.POST['movie']
            room = request.POST['room']
            date = request.POST['date']
            hour = request.POST['hour']
            price = request.POST['price']
            rows = int(request.POST['rows'])
            cols = int(request.POST['cols'])

            date = date.replace('p.m.', 'PM')
            date = date.replace('a.m.', 'AM')

            try:
                date = datetime.datetime.strptime(date, "%B %d, %Y, %I:%M %p")
                date = date.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                try:
                    date = datetime.datetime.strptime(date, "%B %d, %Y, %I %p")
                    date = date.strftime("%Y-%m-%d %H:%M")
                except Exception as e:
                    pass

            query_show = Show.objects.filter(movie_id__name=movie, room_id__name=room, hour_begin__icontains=hour,
                                             date__icontains=date, movie_id__price=price, room_id__row_sits=rows,
                                             room_id__column_sits=cols)
            if query_show.count():
                seats = list()
                tickets = list()
                show_data = query_show.last()
                query_tickets = Ticket.objects.filter(show_id=show_data.id)

                for ticket in query_tickets:
                    tickets.append((ticket.row_num, ticket.col_num))

                for i in range(rows):
                    for j in range(rows):
                        if (i, j) in tickets:
                            seats.append((i + 1, j + 1, 'booked'))
                        else:
                            seats.append((i + 1, j + 1, 'free'))

                seats = [seats[i:i + rows] for i in range(0, len(seats), rows)]

                context = {
                    'show_id': show_id,
                    'movie': movie,
                    'room': room,
                    'date': date,
                    'hour': hour,
                    'price': price,
                    'rows': [i + 1 for i in range(rows)],
                    'cols': [i + 1 for i in range(cols)],
                    'seats': seats
                }
                return render(request, 'program/booking.html', context)
            else:
                return redirect('program')
    else:
        return redirect('program')
