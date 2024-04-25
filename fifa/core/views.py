from django.shortcuts import render, redirect
import numpy as np
import pandas as pd
from core.ultimateteam import UltimateTeamSelector
from django.contrib import messages
import pickle

# Create your views here.

def home_view(request):
    return render(request, 'core/home.html', context={})

def player_position_view(request):
    if request.method == "GET":
        return render(request, 'core/player_position.html', context={})

    if request.method == "POST":
        pace = request.POST.get('pace')
        shooting = request.POST.get('shooting')
        passing = request.POST.get('passing')
        dribbling = request.POST.get('dribbling')
        defending = request.POST.get('defending')
        physicality = request.POST.get('physicality')
        player_skill = request.POST.get('player_skill')
        player_attacking = request.POST.get('player_attacking')
        player_movement = request.POST.get('player_movement')
        player_power = request.POST.get('player_power')
        player_mentality = request.POST.get('player_mentality')
        player_defending = request.POST.get('player_defending')
        player_goalkeeper = request.POST.get('player_goalkeeper')

        model = pickle.load(open('model.sav', 'rb'))
        attribute_list = [pace, shooting, passing, dribbling, defending, physicality, player_skill, player_attacking, player_movement, player_power, player_mentality, player_defending, player_goalkeeper]
        attribute_list = [int(i) for i in attribute_list]
        pre_player_position = model.predict([attribute_list])[0]
        return render(request, 'core/player_position.html', context={'pre_player_position': pre_player_position})

def players_list_view(request):
    if request.method == "GET":
        country_list = ['Argentina', 'Australia', 'Austria', 'Belgium', 
                        'Brazil', 'Chile', 'Colombia', 'Denmark', 'England', 
                        'France', 'Germany', 'Ghana', 'Italy', 'Korea Republic', 
                        'Mexico', 'Netherlands', 'Norway', 'Poland', 'Portugal', 
                        'Republic of Ireland', 'Russia', 'Saudi Arabia', 'Scotland', 
                        'Serbia', 'Spain', 'Sweden', 'Switzerland', 'United States', 
                        'Uruguay', 'Wales']
        
        return render(request, 'core/index.html', context={'country_list': country_list})
    
    if request.method == "POST":
        total_credit = 1000
        positions = ['Striker', 'Midfielder', 'Defender', 'Goalkeeper']
        
        df = pd.read_csv('core/web_fifa.csv')
        
        # Get all top players according to country name
        country_name = request.POST.get('country_name', None)
        if country_name is not None:
            df = pd.read_csv('core/web_fifa.csv')
            players_dict = {}
            uts = UltimateTeamSelector(df, total_credit, country_name)
            players_dict = uts.get_players(df)
            return render(request, 'core/index.html', context={'players_dict': players_dict})

        # Create 11 players team from top players according to the team formation
        selected_players = request.POST.getlist('selected_players', None)
        formation = request.POST.get('formation', None)
        if formation is not None:
            counts = [int(count) for count in formation.split(",")]
            selected_players = df[df['short_name'].isin(selected_players)]
            request.session['selected_players'] = selected_players.to_dict(orient='records')
            check_players = selected_players['player_positions'].value_counts().to_dict()
            pos_count = dict(zip(positions, counts))

            if not sorted(check_players.items()) == sorted(pos_count.items()):
                messages.add_message(request, messages.ERROR, f'Select players according to the team formation')
                return redirect('players_list')
            
            selected_players_credit = sum(selected_players['credit'])
            if total_credit < selected_players_credit:
                messages.add_message(request, messages.ERROR, f'You do not have enough credits to select players')
                return redirect('players_list')
            else:
                remaining_creadits = total_credit - selected_players_credit
                request.session['remaining_creadits'] = remaining_creadits
            
            country_name = selected_players.iloc[0]['nationality']
            uts = UltimateTeamSelector(df, total_credit, country_name)
            players_dict = uts.get_players(df)
            players_dict = [item for sublist in players_dict.values() for item in sublist]
            available_players = pd.DataFrame(players_dict)
            remaining_players = available_players.merge(selected_players, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
            remaining_players = remaining_players.to_dict(orient='records')
            remaining_players = sorted(remaining_players, key=lambda x: x['player_positions'])
            return render(request, 'core/index.html', context={'remaining_players': remaining_players})
        
        selected_sub_players = request.POST.getlist('selected_sub_players', None)
        if selected_sub_players is not None:
            selected_sub_players = df[df['short_name'].isin(selected_sub_players)]
            selected_subs = selected_sub_players.to_dict(orient='records')
            request.session['selected_sub_players'] = selected_subs

            selected_players_credit = sum(selected_sub_players['credit'])
            remaining_creadits = request.session.get('remaining_creadits', None)
            if remaining_creadits < selected_players_credit:
                messages.add_message(request, messages.ERROR, f'You do not have enough credits to select players')
                return redirect('players_list')
            else:
                remaining_creadits = remaining_creadits - selected_players_credit
                request.session['remaining_creadits'] = remaining_creadits
            
            remaining_creadits = request.session.get('remaining_creadits', None)
            selected_players = request.session.get('selected_players', None)
            selected_sub_players = request.session.get('selected_sub_players', None)
            ultimate_team = True

            request.session.clear()

            context={'remaining_creadits': remaining_creadits,
                     'selected_players': selected_players,
                     'selected_sub_players': selected_sub_players,
                     'ultimate_team': ultimate_team
                     }
            return render(request, 'core/index.html', context=context)