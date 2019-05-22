import requests
luis_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/fc1607f9-58d5-4aec-bf84-b8ef7421a200?verbose=true&timezoneOffset=-360&subscription-key=42a6ebf02a1d4566a958dbd421dd1380&q="
stats_url = "http://lookup-service-prod.mlb.com/"
player_info = "json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part="
player_stats = "json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2017'&player_id="

def main():
    while True:
        query = input("\nPlease enter your query: \n\n")
        print()
        url = luis_url + query
        json = get_json(url) 
        
        try:
            intent = json['topScoringIntent']['intent']
            player_name = json['entities'][0]['entity']
            player_id = get_player_id(player_name)

            if (player_id == '0'):
                print("Couldn't find that player. Please try again.")
                continue

            if (intent == "FindBattingAverage"): # FindBattingAverage
                avg = get_statistic(player_id,'avg')
                print("\t" + player_name + " is batting " + avg)
            elif (intent == "FindHomeRuns"): # FindHomeRuns
                hr = get_statistic(player_id,'hr')
                print("\t" + player_name + " has " + hr + " home runs")
            else: # None
                print("\tCouldn't understand your query, to exit press CTRL+C.")
        except Exception as error:
            print(error)

def get_json(url):
    response = requests.get(url)
    try:
        json = response.json()
        return json
    except:
        return {}

def get_home_runs(player_id):
    url = stats_url + player_stats + player_id
    json = get_json(url)
    try:
        homeruns = json['sport_hitting_tm']['queryResults']['row']['hr']
    except Exception as e:
        homeruns = '0'
    finally:
        return homeruns

def get_statistic(player_id, statistic):
    url = stats_url + player_stats + player_id
    json = get_json(url)
    try:
        res = json['sport_hitting_tm']['queryResults']['row'][statistic]
    except Exception as e:
        res = '0'
    finally:
        return res

def get_batting_average(player_id):
    url = stats_url + player_stats + player_id
    json = get_json(url)
    try:
        avg = json['sport_hitting_tm']['queryResults']['row']['avg']
    except Exception as e:
        avg = '0'
    finally:
        return avg


def get_player_id(player_name):
    url = stats_url + player_info + "\'" + player_name + "\'"
    json = get_json(url)
    try:
        player_id = json['search_player_all']['queryResults']['row']['player_id']
    except Exception as e:
        player_id = '0'
    finally:
        return player_id

if __name__ == "__main__":
	main()