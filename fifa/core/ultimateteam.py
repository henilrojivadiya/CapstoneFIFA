class UltimateTeamSelector:
    def __init__(self, df, total_credit, country_name) -> None:
        self.df = df
        self.total_credit = total_credit
        self.country_name = country_name  

    def get_players(self, df):
        positions = ['Striker', 'Midfielder', 'Defender', 'Goalkeeper']
        players_dict = {}
        for position in positions:
            available_players = df[df['nationality'] == self.country_name][df['player_positions'].str.contains(position)].sort_values(by='credit', ascending=False).head(10)
            players_dict[position] = available_players.to_dict(orient='records')
        return players_dict
    
    
# class UltimateTeamSelector:
#     def __init__(self, dataset, total_credit, country_name):
#         self.dataset = self.filter_by_country(dataset, country_name)
#         self.total_credit = total_credit
#         self.selected_players = list()
#         self.substitute_players = list()

#     def filter_by_country(self, dataset, country_name):
#         return dataset[dataset['nationality'] == country_name]

#     def sort_players_by_credit(self):
#         return self.dataset.sort_values(by='credit', ascending=False)

#     def select_players(self, position, count):
#         available_players = self.dataset[self.dataset['player_positions'].str.contains(position)].head(10) if position != 'Substitute' else pd.concat(self.substitute_players, ignore_index=True)
#         available_players.index = available_players[['short_name', 'player_positions', 'credit']].reset_index(drop=True).index + 1
#         print(f"\n\n Select {count} {position}s from the top players:")
#         print(available_players[['short_name', 'player_positions', 'credit']])
        
#         while True:
#             choice = input("Enter comma-separated player numbers (or 0 to skip): ")
#             choices = [int(choice) for choice in choice.split(",") if choice.isdigit()]
#             if 0 in choices:
#                 break
#             else:
#                 selected_players = available_players.iloc[[item - 1 for item in choices]]
#                 total_credit_required = selected_players['credit'].sum()
#                 if total_credit_required <= self.total_credit and len(selected_players) == count:
#                     self.selected_players.append(selected_players)
#                     self.total_credit -= total_credit_required
#                     print("Selected players added to the team!")
#                     print(f"Remaining credit: {self.total_credit}")

#                     if position != 'Substitute':
#                         remaining_players = available_players.merge(selected_players, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
#                         self.substitute_players.append(remaining_players)
                    
#                     break
#                 else:
#                     print("Invalid selection. Please try again.")
        
    
#     def select_substitutes(self):
#         count = input("\n\n Number of substitutes you want (or 0 to skip): ")
#         self.select_players('Substitute', int(count))
        

#     def build_ultimate_team(self, formation):
#         positions = ['Striker', 'Midfielder', 'Defender', 'Goalkeeper']
#         counts = [int(count) for count in formation.split(",")]
#         for position, count in zip(positions, counts):
#             self.select_players(position, count)
        
#         if len(self.selected_players) == 4:
#             self.select_substitutes()
            

#     def display_team(self):
#         print("\nFinal selected team:")
#         final_selected_players = pd.concat(self.selected_players, ignore_index=True)
#         final_selected_players.index = final_selected_players[['short_name', 'player_positions', 'credit']].reset_index(drop=True).index + 1
#         print(final_selected_players[['short_name', 'player_positions', 'credit']])
#         print(f"\nRemaining credit: {self.total_credit}")
    
    
# # total_credit = 1000
# # country_name = input("Enter country name: ")
# # formation = input("Enter team formation (e.g., 4,3,3,1): ")
# # ultimate_team_selector = UltimateTeamSelector(df, total_credit, country_name)
# # ultimate_team_selector.build_ultimate_team(formation)
# # ultimate_team_selector.display_team()