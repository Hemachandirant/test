from datetime import datetime
import pytz
from requests.auth import HTTPBasicAuth
from langchain.agents import initialize_agent, AgentType, Tool
from langchain import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
from datetime import datetime, timedelta
import pytz     
import requests
import json
import os
import re



class OpenAIFunctions:
    accessToken = "EwB4A8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAbbOpdy02fizvO6P4bAajN735LjBbxuu1X0mqERUkcyFc8DduW3KbMOO+u5HCLfp7wZlR7jfVk4+OCvjG+1KUnVm6KjrItTnqg/GKJzSvXHTBtrToTQGglw1gRf+LJp25yuO7ZUdUV6OIGnTfjjax8xFyvIiBPQbdQQAWlQaDYklpeimuenDOwA2+J7iLtMYHW21nby5pwx8JAtJ5xVmXenw0zj+0lHTBGQ33pMXCXRGbVbDuysx9DbTjbDdOeGfu09kzw61je5iQL38l/bbHR4VIFf7Y9OEKt7ifcx+3yODdBkSkqURr96gU6jV3mgVeLeWj6ISGy08L2n2eu/6OjUDZgAACJGDDIdLNd1cSAK70moU8TZ6OHklztLi+rR2Ta1x23aKErVkZeiKHZBY/l4qQ94fuHqUOOrLMsijRMdS69l0+6xqA0f9gGe7ctPWqj+DluJwUSmhkrlFfbp6C1JX7CDCnQIg0WTazoQlYSwvPvy3OC9UhSxaDbnYUqNJHczm6DA9/8fdOSJMUIaUTOkO1OnAm7uFDlCSo8C9F06mi13niVcr7EzjmKvC4URTGdrqLWnbUyHaoucaIc2mGGg4mN2vlCSyP3Czipq8r6c2+qaIhO3253qYatzTIzADjX/jSO1CfhXQ8tVMJmRJDYSvIIa8CtBtDLAzzQT2zASyVa/4qX2HBS+tF8fdLllc7ooT7POtcXsqY5AnOIn8NsXpzoI0vKcfozIHurybrByh95E91pCxvdYSA8Qaw8ZYgZWObEcowbifL838TfNIIiGy0bQ58C83rKPH3mhU2lvSXxdn0ECG9YwLOXT3sU+f6MbLqqoZttMCasLA7d/Rt8r7pBl/6vvAH250mkvVVTEhzM0ON81RAQKUV0euJ1+6xcJrl8HYbhaweJTtDutznonzYPk/RPFVRzzQwbfJx+XIteAdsgb7Ia8DO1Vl8oo4H9goXrN+6HkXDvM1Hw8LUqNfjXYAVeIT+mZehCGb9QpviGRu179P7xdR7zUCpvdpRFAoUwrMwI8kLPOlBtCTpRIpOGTXcFch0AaIdZ5vwmvv+VCZAsC+2x3ealxJBIKyuFKXIezdtLFwGX7yOrrwRiy2nNe+V4Ssq0vUhiXh/LK8c1Oko1WXEIYC"
    meeting = "EwCgA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAVTjs1ciWmAtpdfCWVgDDTrKUVi8JDSTTcxHxQvdS3rAECfIBIjh3/QePkiUPVhcYS4ST22JXgvpBq8sWC2JNKpnRAVAaf6RC4P3xt/RBoLvSx1FxcA8i7qeqY4KYHCoxMts5QbUzn7VVOJnzgyiHYPzLEUFs5OvXmoiALTVm6cVibFeHcvyGnVCwkEivVkEY+hX/VEgQpioq7ESjkHEZuVnAP5lajkVbAH4TmhQhShD1L5ATGCZj/10OouYEGiYG5Fi7Q7t2cuzTGvpEX5OCKrXMUs6pIQ27hgxJGPf+yseeR9v628OeZQVHPuYRy75XFUpO4nbCeiJLwt4unwC+g8DZgAACNca9ZN6x4CycAIcEykJR+BOsQkDZ1PmdXE1XvjuIr2NsG2SSLsLXL49tSGr22YpfmLL+ObtBWVYstTOP4S0MSlHaRbccmUPvlWfilAXZIOo2TLEy8sZC51ziSWLNob2Wwek/oJKNF1dWL+BZxX9lEVhzuNJw9bJccWTMN+svdWYkv9NqkkZwm9HH9GOnMWfaxP2d8/olWOIaHnHApz80d7otrRrbIlRY9GEh+1RZEnmcVaFiqsNmRzXePjcoQ26UTy/eNsX7dZc+X9TdvsG2spPskCkTnnoeGHQgrhNEVUPxTmPYuG5hho/eipeBtgRbdLw2ToeR4EU2W8EayAQnnAWW7xf22HNq+NwVOoeKjKDATsyVxo9rtTuNPqw4RQsVJDXJ7oZMbAM2695I0kzDfjKZvGJkOWiUPTNO2DH96Px3YMEzpc5Ai2ofcQCkMzkVz1OQYBv3G75qYjZaXilYy2avJ2Z29j+ji9ObvC92u05tkxoPXKw4PO1JiXlAlBVhClJ105LFEtHHyQgzSkV88PSuVKaWlmCqukOw7amqB/buVChgzO4n64XSR9UqAhvKf2LPMsNSwdjY8u52r5NoCdzg5gAW/XPWjfZxwjkAPxQNrQgX1S+GvMT+bVgJiNMbnWw9RdM85tLme8XB5Y1ZJMU6LzXyKD5FZCFX1IKeWeLajk276JmDj6WNIbNRTvlgQdx72Ebx9H19aEaIr9+KaLDUYCzgllW6zRm1+0vWgHIaYRhLYMyPJAH/jleKYyfXoSfzEmeOxwt0rjxMRD4gP316J1rjaXsc9ZV78QtOYmsn61bIzLgp2Li4nVbWHNKkTHIPBmGzGrzA9OqAg=="
    getEvents ="EwCYA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAXyRdIQJ+N4AT9gWcR9jB3jU8qrjn7e3fD9DlX8o4kVbQ1y2JFQjEoxv6Vxomc5l4MZJB1mog+kztOMPWablFSpktubqQJGdmAUV+tgBPPu4lxH6ZLOn4axiGsxyJjb7C+43hC33IcWCVmEM/9gEoCE48vOb1hZ1oFRdGP8bZebBjtgXrlCMa3OViJJd+xVLNiH/PTFFuY0zkLnIFwON3ErpV9j0HG8XMm0zVxcONjdyfy5VRUMKtrs6YgYDISmzFDpCr8XEwNhJ18bycgfd6ZhHoanWtDBPvF3z56DyvVHvn7Wq4MGajXlCJmLDSIXLGuVD69rPmVjlyvYnRxqf4yYDZgAACHBqa/Ko6tTJaAIB+4cS9VWLYvH7cvYR0PIQGC+DXNiz0Je7s/PwiFKwxRwDlivFClGYXcimcnZ/jofwnEXzHH5g59siqcKqNNNyDApK9huhi+peTiBm2INMlUuby4qX7dBsOkcMWnQ9XHxPnqnRS/tK+edCI1N1rujfztOAu9y/ur6qfJGA4ET8mSqlRILRit9x9dGQsFaaNFy74IOZFErHT2HNf8mVVAlLnVponyT9AFsqFGdYESU9WPheei/SegI0So8ot5nZAZsXJsRLdPbrxX+ObgDONlJyvv0On7CE9F3k9nCMaQBRSiYPiuqtkYNRB313+1uQUzH7f9cW9YpH3gkvCkSHpTwgY573CeKCXbiqhQj06hNGLOxHd57+VuOWCT9suF0lnsAqZQNAUqM46FJcd6bqNZw9coT8vG1fA+rscTYN0xzjD69RTBOqNeWvjWIGEj3tp+x9cgTelBful6kADmdOkTk+h6V3YsqvKL1nz/VxZPx5tXp3fK3YzbUW31HLYSpIwi7wj3mKZimwUv99eXA96OChuLd7FGyKfORvWDfzUUoZJ/8VisyHbleqkDAsJmUJrmoQNGWrnbOPiBkiO8eZ6VFtz1Ewu+UXvoxnPlPADAB7yRYTet7TldPLvPIq1VJ7b9jiXXvC57C1SAIXUiXtLAbeKYGVl92gR7Vfz4VmOhzJ0dpp4OYV+cZyjLok/61HS01Yy71btDT5JW5h8kLNo2ReXqYQxH1fj+Z8eK9lps4+DNuTXQ2DowgHDhpAPdTDnN9BcbWykYhUZJYucdQxIJjphXDs8r9xS/Pw+b80IMA/ZWMJqOhwHSV5pgI="

    @staticmethod
    def get_current_weather(longitude, latitude):
        """Get the current weather for a location"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "timezone": "Europe/Berlin",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return json.dumps(data["current_weather"])
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return json.dumps({"error": "Failed to get weather"})

    @staticmethod
    def get_search_results(query):
        """Get search results for a query"""
        try:
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
            search = SerpAPIWrapper(
                serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
            )
            tools = [
                Tool(
                    name="Search",
                    func=search.run,
                    description="useful for when you need to answer questions about current events. You should ask targeted questions",
                )
            ]
            agent = initialize_agent(
                tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
            )
            res = agent.run(query)
            return json.dumps(res)
        except Exception as e:
            print(f"Error getting search results: {e}")
            return json.dumps({"error": "Failed to get search results"})
        
    @staticmethod
    def search_images(query, max_results=10):
        """Search for images using the SERPAPI image search service"""
        try:
            # Initialize SERPAPI client with your API key
            serpapi_api_key = os.getenv("SERPAPI_API_KEY")
            search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

            # Define the parameters for the image search
            params = {
                "q": query,
                "tbm": "isch",  # Image search
                "num": max_results,  # Number of results to retrieve
            }

            # Perform the image search
            response = search.run(params)

            return json.dumps(response)
        except Exception as e:
            print(f"Error searching images: {e}")
            return json.dumps({"error": "Failed to search for images"})
        
    @staticmethod
    def service_now_ticket_creation(short_description, description):
        """Create a new servicenow ticket"""

        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

        uri = "https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_display_value=true"

        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        # define payload for request, note we are passing the sysparm_action variable in the body of the request

        payload = {"short_description": short_description, "description": description}

        r = requests.post(
            url=uri, data=json.dumps(payload), auth=auth, verify=False, headers=headers
        )

        content = r.json()

        return json.dumps(content)
    
    @staticmethod
    def get_incident_status_by_number(incident_number):
        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

        uri = f"https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_query=numberLIKE{incident_number}^ORDERBYDESCsys_created_on&sysparm_display_value=true"

        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        r = requests.get(url=uri, auth=auth, verify=False, headers=headers)

        content = r.json()

        return json.dumps(content)
    @staticmethod
    def get_recent_incidents_status(number_of_incidents):
        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

        uri = f"https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_query=sys_created_bySTARTSWITHadarsh^ORDERBYDESCsys_updated_on^active=true&sysparm_limit={number_of_incidents}"
        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        r = requests.get(url=uri, auth=auth, verify=True, headers=headers)

        content = r.json()

        incidents = []
        for incident in content["result"]:
            status = incident["state"]
            incident_number = incident["number"]
            short_description = incident["short_description"]
            comments = incident["comments"]
            description = incident["description"]
            sys_id = incident["sys_id"]

            # Storing the extracted fields in a dictionary
            incident_dict = {
                "status": status,
                "incident_number": incident_number,
                "short_description": short_description,
                "comments": comments,
                "description": description,
                "sys_id": sys_id
            }

            # Adding the dictionary to a list of incidents
            incidents.append(incident_dict)


        print("Response Status Code: " + str(content))

        return json.dumps(incidents)

    @staticmethod
    def add_comment_to_incident(incident_number, comment):
        content_list = OpenAIFunctions.get_incident_status_by_number(incident_number)

        # Ensure content_list is a list and not a JSON string
        if isinstance(content_list, list):
            content = content_list[0]  # Assuming the list contains a single dictionary
            status = content.get("result", {}).get("state")
            incident_number = content.get("result", {}).get("number")
            short_description = content.get("result", {}).get("short_description")
            comments = content.get("result", {}).get("comments")
            description = content.get("result", {}).get("description")
            sys_id = content.get("result", {}).get("sys_id")

            auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")
            uri = f"https://wiprodemo4.service-now.com/api/now/table/incident/{sys_id}?sysparm_display_value=true"
            headers = {
                "Accept": "application/json;charset=utf-8",
                "Content-Type": "application/json",
            }
            payload = {
                "comments": comment
            }
            r = requests.patch(url=uri, auth=auth, verify=True, headers=headers, json=payload)
            content = r.json()
            print("Response Status Code: " + str(content))
            return json.dumps(content)
        else:
            # Handle the case where content_list is not a list (e.g., an error response)
            return "Invalid content data"
        
    # @staticmethod
    # def get_access_token():
    #     # Define the token endpoint and your Azure AD application credentials
    #     token_url = "https://login.microsoftonline.com/fd50ca56-92c4-4a17-8397-ca4cf2991191/oauth2/v2.0/token"
    #     client_id = "30296a67-052d-4217-8a6c-c8c984cb98c6"
    #     client_secret = "_Ot8Q~2bhZloCgOChrwIVrO0l_nIEZ01hI0OPcMY"
    #     scope = "https://graph.microsoft.com/.default"

    #     # Create the request payload
    #     payload = {
    #         "grant_type": "client_credentials",
    #         "client_id": client_id,
    #         "client_secret": client_secret,
    #         "scope": scope
    #     }

    #     try:
    #         # Send the POST request to obtain the access token
    #         response = requests.post(token_url, data=payload)

    #         # Check if the request was successful (status code 200)
    #         if response.status_code == 200:
    #             # Parse the JSON response
    #             token_data = response.json()

    #             # Extract the access token from the response
    #             access_token = token_data.get("access_token")

    #             return access_token
    #         else:
    #             print("Failed to obtain access token. Status code:", response.status_code)
    #             return None
    #     except Exception as e:
    #         print("An error occurred:", str(e))
    #         return None


    @staticmethod
    def send_email_via_graph_api(recipient_email, subject, message_body):
        try:
            access = OpenAIFunctions.accessToken
        # Microsoft Graph API endpoint for sending emails
            api_url = "https://graph.microsoft.com/v1.0/me/sendMail"

            # Create the email message payload
            email_data = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "Text",
                        "content": message_body
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": recipient_email
                            }
                        }
                    ]
                }
            }

            headers = {
                "Authorization": f"Bearer {access}",
                "Content-Type": "application/json"
            }

            # Send the email using the Graph API
            response = requests.post(api_url, headers=headers, data=json.dumps(email_data))

            if response.status_code == 202:
                # Return a valid JSON response even in the case of success
                return json.dumps({"status": "Email sent successfully!"})
            else:
                error_message = f"Failed to send email. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
    
    @staticmethod
    def schedule_meeting_via_graph_api( recipient_email, subject, start_time, end_time, location):
        try:
        # Microsoft Graph API endpoint for scheduling meetings
            api_url = "https://graph.microsoft.com/v1.0/me/events"
            access_token = OpenAIFunctions.meeting
            
            ist = pytz.timezone('Asia/Kolkata')

            # Convert start_time and end_time to naive datetime objects
            start_time_naive = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
            end_time_naive = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')

            # Set the timezone to IST
            start_time_ist = ist.localize(start_time_naive, is_dst=None)
            end_time_ist = ist.localize(end_time_naive, is_dst=None)

            # Format the datetime objects in UTC format
            start_time_utc_str = start_time_ist.astimezone(pytz.UTC).isoformat()
            end_time_utc_str = end_time_ist.astimezone(pytz.UTC).isoformat()

            # Create the meeting request payload
            meeting_data = {
                "subject": subject,
                "start": {
                    "dateTime": start_time_utc_str,
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_time_utc_str,
                    "timeZone": "UTC"
                },
                "location": {
                    "displayName": location
                },
                "attendees": [
                    {
                        "emailAddress": {
                            "address": recipient_email
                        }
                    }
                ],
                "isOnlineMeeting":True,
                "allowNewTimeProposals": True,
                # "onlineMeetingProvider": "teamsForPersonal"
            }

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            # Send the meeting request using the Graph API
            response = requests.post(api_url, headers=headers, data=json.dumps(meeting_data))

            if response.status_code == 201:
                # Return a valid JSON response even in the case of success
                return json.dumps({"status": "Meeting scheduled successfully!"})
            else:
                error_message = f"Failed to schedule meeting. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
        
    @staticmethod
    def cancel_meeting_by_name_via_graph_api(meeting_name):
        try:
            # Microsoft Graph API endpoint for retrieving events (meetings)
            api_url = "https://graph.microsoft.com/v1.0/me/events"

            access_token = OpenAIFunctions.meeting

            headers = {
                "Authorization": f"Bearer {access_token}",
            }

            # Send a GET request to retrieve the user's events (meetings)
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                events = response.json().get("value", [])

                # Find the meeting with the specified name
                for event in events:
                    if event.get("subject") == meeting_name:
                        meeting_id = event.get("id")
                        
                        # Use the meeting ID to cancel the meeting
                        cancel_url = f"https://graph.microsoft.com/v1.0/me/events/{meeting_id}"
                        cancel_response = requests.delete(cancel_url, headers=headers)

                        if cancel_response.status_code == 204:
                            return json.dumps({"status": "Meeting canceled successfully!"})
                        else:
                            error_message = f"Failed to cancel meeting. Status code: {cancel_response.status_code}"
                            return json.dumps({"error": error_message, "response": cancel_response.text})

                # If the meeting with the specified name is not found
                return json.dumps({"error": f"Meeting with name '{meeting_name}' not found."})
            else:
                error_message = f"Failed to retrieve events. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
        
    def find_meeting_times(participants, start_time, end_time):
    # Define the API endpoint
        api_endpoint = "https://graph.microsoft.com/v1.0/me/findMeetingTimes"
        access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IlFoVmg5ZlN6T3pHZndlQW9hVm4wd3JOQ3BDY0ZUdnNuZi1keWNWSFJZZzgiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMGZiZGUyYi1kZTJiLTRmZWEtODMyMC0zMzczYzIyNzg1NzQvIiwiaWF0IjoxNjk3MTc0MzQwLCJuYmYiOjE2OTcxNzQzNDAsImV4cCI6MTY5NzI2MTA0MCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQTVmRWxWcGhTMFpSZTdMc1o0R01FVlcvTjdPWURHd09NcnVHdkZLcEdOMkR2ZlppTzlkZ0tVaHpaWG1OREJkcGlZREl6WlgxWllDdnhnUlZsSVkwZGJ3UEhyL2V6OCtPQ2ZQV3pVUnZUMVpnPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiVCIsImdpdmVuX25hbWUiOiJIZW1hY2hhbmRpcmFuIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMjIzLjE4Mi4yMzEuODEiLCJuYW1lIjoiSGVtYWNoYW5kaXJhbiBUIiwib2lkIjoiYmEwMGZiNzYtNGEzZi00YjliLTk5MmEtNWRlMDE5Yjc0NTFmIiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAyRjg1NkFGNUUiLCJyaCI6IjAuQWIwQUs5NzdvQ3ZlNmstRElETnp3aWVGZEFNQUFBQUFBQUFBd0FBQUFBQUFBQURMQUc0LiIsInNjcCI6IkNhbGVuZGFycy5SZWFkLlNoYXJlZCBDYWxlbmRhcnMuUmVhZFdyaXRlLlNoYXJlZCBvcGVuaWQgcHJvZmlsZSBVc2VyLlJlYWQgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJXQ2FrNVp0NXIzRkgyengwVlRhMHB3NVZCdGExWUloaGl4WFlkMnd5VlRRIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6Ik5BIiwidGlkIjoiYTBmYmRlMmItZGUyYi00ZmVhLTgzMjAtMzM3M2MyMjc4NTc0IiwidW5pcXVlX25hbWUiOiJIZW1hY2hhbmRpcmFuQDhrMGdmMS5vbm1pY3Jvc29mdC5jb20iLCJ1cG4iOiJIZW1hY2hhbmRpcmFuQDhrMGdmMS5vbm1pY3Jvc29mdC5jb20iLCJ1dGkiOiJmdDhJZUdvWEcwR1NJOFZxZjYwckFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyI2MmU5MDM5NC02OWY1LTQyMzctOTE5MC0wMTIxNzcxNDVlMTAiLCJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJ6cjVPdklsV3F3OE5rNEs3X1hFZWVlbUhSUHFOdk92MHp0UERaWVNwZGljIn0sInhtc190Y2R0IjoxNjk1NTEwMzY5fQ.b98U17d61oWaO9iZcIkTGM_2CP4O-XOLazwHitygjp8hlG2yPmuZ79-aarVDxMYqiyZzv3bOPzzM8FTJqGd2jN66WnCyWyl_xLq_ic-2mClLAPoYFArvXMVMicAqLoA9PAbv23bYO7nLTFTWlznPCOALH0dQ8xqleMI_JPa3DQ-ljqPHTB5cjZmbSNxlb7ZELUZcT-1yDDzaLOwM4J2C_SOU8FhiBPH8jvF2FofLC9yGcxwkxbGEzhVPl-j7w3YVW0DiwOq1VesVTAjx5uZJ9hSaYnU5S-Vt4QuOB0tAw0Or1DTTdk_RyvwSxkU9Kfg9HaLWXIgfeWR7fWfwHwPIJA"

        # Define the request headers
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }

        # Create the attendees list for the request payload
        attendees = [{"emailAddress": {"address": email}, "type": "required"} for email in participants]

        # Define the request payload
        payload = {
            "attendees": attendees,
            "timeConstraint": {
                "activityDomain": "work",
                "timeslots": [
                    {
                        "start": {
                            "dateTime": start_time,
                            "timeZone": "UTC"
                        },
                        "end": {
                            "dateTime": end_time,
                            "timeZone": "UTC"
                        }
                    }
                ]
            }
        }

        # Make the API request
        response = requests.post(api_endpoint, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Extract and print availability timings in IST
            availability_timings = []

            for suggestion in data.get("meetingTimeSuggestions", []):
                start_time_utc = suggestion.get("meetingTimeSlot", {}).get("start", {}).get("dateTime", "")
                end_time_utc = suggestion.get("meetingTimeSlot", {}).get("end", {}).get("dateTime", "")

                if start_time_utc and end_time_utc:
                    # Remove the fractional part of seconds
                    start_time_utc = re.sub(r'\.\d+', '', start_time_utc)
                    end_time_utc = re.sub(r'\.\d+', '', end_time_utc)

                    # Convert UTC times to IST
                    ist = pytz.timezone('Asia/Kolkata')
                    start_time_ist = datetime.strptime(start_time_utc, "%Y-%m-%dT%H:%M:%S")
                    end_time_ist = datetime.strptime(end_time_utc, "%Y-%m-%dT%H:%M:%S")
                    start_time_ist = ist.localize(start_time_ist).astimezone(ist)
                    end_time_ist = ist.localize(end_time_ist).astimezone(ist)

                    availability_timings.append((start_time_ist, end_time_ist))

            # Prepare the response as a JSON object
            response_data = {
                "status": "Success",
                "availability_timings": [(str(start), str(end)) for start, end in availability_timings]
            }
        else:
            # Prepare an error response
            response_data = {
                "status": "Error",
                "message": f"Error: {response.status_code} - {response.text}"
            }

        # Return the response as JSON
        return json.dumps(response_data)

        


    # @staticmethod
    # def get_free_time_slots(user_email):
    #     user_email = "david@hemac140gmail.onmicrosoft.com"

    #     # Set the access token obtained from authentication
    #     access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InRVcFotR1Ztd1lOVHlUWTJ3b3JNRklHcWV5aGtxWjhnWnJZd2F2enJhbG8iLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMGZiZGUyYi1kZTJiLTRmZWEtODMyMC0zMzczYzIyNzg1NzQvIiwiaWF0IjoxNjk3MDg3ODM1LCJuYmYiOjE2OTcwODc4MzUsImV4cCI6MTY5NzE3NDUzNSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQXhYZHJqVnVTdkg3Um04UzkxTnUveVNQRnpUTm4yRkJVMGhaa1lFdEdHb3k2cVBqeWZLbEhtdHJkT3FjYWllWm9vcUF3Y2ZCUFRDQ3JCdmpPUVhjRmRVL014NmpuNXoybGFTMjRIYlhtRXpzPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiVCIsImdpdmVuX25hbWUiOiJIZW1hY2hhbmRpcmFuIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTY1LjIyNS4xMDQuMTAwIiwibmFtZSI6IkhlbWFjaGFuZGlyYW4gVCIsIm9pZCI6ImJhMDBmYjc2LTRhM2YtNGI5Yi05OTJhLTVkZTAxOWI3NDUxZiIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMjAwMkY4NTZBRjVFIiwicmgiOiIwLkFiMEFLOTc3b0N2ZTZrLURJRE56d2llRmRBTUFBQUFBQUFBQXdBQUFBQUFBQUFETEFHNC4iLCJzY3AiOiJDYWxlbmRhcnMuUmVhZC5TaGFyZWQgQ2FsZW5kYXJzLlJlYWRXcml0ZS5TaGFyZWQgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkIGVtYWlsIiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoiV0NhazVadDVyM0ZIMnp4MFZUYTBwdzVWQnRhMVlJaGhpeFhZZDJ3eVZUUSIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJOQSIsInRpZCI6ImEwZmJkZTJiLWRlMmItNGZlYS04MzIwLTMzNzNjMjI3ODU3NCIsInVuaXF1ZV9uYW1lIjoiSGVtYWNoYW5kaXJhbkA4azBnZjEub25taWNyb3NvZnQuY29tIiwidXBuIjoiSGVtYWNoYW5kaXJhbkA4azBnZjEub25taWNyb3NvZnQuY29tIiwidXRpIjoiVDlfX19TbDBQVVNZczZIUEFIcDdBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiNjJlOTAzOTQtNjlmNS00MjM3LTkxOTAtMDEyMTc3MTQ1ZTEwIiwiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEiLCJ4bXNfc3QiOnsic3ViIjoienI1T3ZJbFdxdzhOazRLN19YRWVlZW1IUlBxTnZPdjB6dFBEWllTcGRpYyJ9LCJ4bXNfdGNkdCI6MTY5NTUxMDM2OX0.VwHfL-9erkUNJLethnfsjT9Uv2AzMfDqpOL88mFKuzO1rvh3k3-IkJB75LxvJgSd4Z3hT0TDp3mm3listUpQzdLLHCOxNrpM7XJBd-YPVBSesenQ-4UCJzi2FpxTlO_0IVbiZj3wGVsMKzSVB_niIeAcwRHWfB3XWoNaNOMRq832AJsc0YPedlRjdIvPGC0c6fC3uzCyGnf7ipg9HwAYDy0AlNVBVOklB25PVOebeKcbMvJXUpVdDS25pjCGYKrjWUKk1oxJoj_AMf2pGxCmegWhuVPP5IYCK6JvZ3jte13s5YmbLOKNBUI5Uqd9HQmxi2cBhghGxvGhL5Dmvx0XvQ"

    #     # Define IST (Indian Standard Time) timezone
    #     ist_timezone = pytz.timezone('Asia/Kolkata')

    #     # Define a function to convert UTC time to IST
    #     def convert_utc_to_ist(utc_time):
    #         return utc_time.astimezone(ist_timezone)

    #     headers = {
    #         "Authorization": f"Bearer {access_token}",
    #         "Content-Type": "application/json",
    #     }

    #     # Microsoft Graph API endpoint for retrieving a user by UPN
    #     user_api_url = f"https://graph.microsoft.com/v1.0/users/{user_email}"

    #     # Send a GET request to retrieve the user's information
    #     response = requests.get(user_api_url, headers=headers)

    #     if response.status_code == 200:
    #         user_data = response.json()
    #         user_id = user_data["id"]
    #         #print(f"User ID for {user_email}: {user_id}")

    #         # Microsoft Graph API endpoint for retrieving events (calendar)
    #         api_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/calendarView"

    #         # Set the time range for which you want to find free time (e.g., from 12:00 AM to 12:00 PM) in IST
    #         now_utc = datetime.now(pytz.utc)
    #         start_time_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    #         end_time_utc = start_time_utc + timedelta(hours=12)

    #         # Format the time range as ISO 8601 strings
    #         start_time_str_utc = start_time_utc.isoformat()
    #         end_time_str_utc = end_time_utc.isoformat()

    #         # Construct the query parameters
    #         params = {
    #             "startDateTime": start_time_str_utc,
    #             "endDateTime": end_time_str_utc,
    #             "$select": "start,end",
    #             "$top": 50,  # Number of events to retrieve (adjust as needed)
    #         }

    #         # Send a GET request to retrieve calendar events for the specified user and time range
    #         response = requests.get(api_url, params=params, headers=headers)

    #         if response.status_code == 200:
    #             events = response.json().get("value", [])

    #             # Convert UTC event times to IST
    #             events = [
    #                 {
    #                     "start_time": convert_utc_to_ist(datetime.fromisoformat(event["start"]["dateTime"][:-1])),  # Remove excessive digits
    #                     "end_time": convert_utc_to_ist(datetime.fromisoformat(event["end"]["dateTime"][:-1])),  # Remove excessive digits
    #                 }
    #                 for event in events
    #             ]

    #             # Create a list of time slots where there are no events
    #             free_time_slots = []
    #             current_time = start_time_utc
    #             for event in events:
    #                 event_start = event["start_time"]
    #                 if current_time < event_start:
    #                     free_time_slots.append({
    #                         "start_time": current_time.isoformat(),
    #                         "end_time": event_start.isoformat(),
    #                     })
    #                 current_time = event["end_time"]

    #             # If there's free time after the last event
    #             if current_time < end_time_utc:
    #                 free_time_slots.append({
    #                     "start_time": current_time.isoformat(),
    #                     "end_time": end_time_utc.isoformat(),
    #                 })

    #             for item in free_time_slots:
    #                 # Convert the strings back to datetime objects
    #                 start_time = datetime.fromisoformat(item['start_time'])
    #                 end_time = datetime.fromisoformat(item['end_time'])
                    
    #                 # Format as needed (IST timezone)
    #                 start_time_str = start_time.astimezone(ist_timezone).strftime('%Y-%m-%d %H:%M:%S')
    #                 end_time_str = end_time.astimezone(ist_timezone).strftime('%Y-%m-%d %H:%M:%S')
    #                 #print(f'Start Time: {start_time_str}')
    #                 #print(f'End Time: {end_time_str}')

    #                 a = []
    #                 a.append(start_time_str)
    #                 a.append(end_time_str)
    #                 #print(a)

    #             # Convert the list of free time slots to a JSON string
    #             free_time_json = json.dumps(a, indent=1)
    #             print(f"Free Time Slots for User  {user_email}:")
    #             print(free_time_json)
    #             return json.dumps(free_time_json, indent=1)

    #         else:
    #             error_message = f"Failed to retrieve events. Status code: {response.status_code}"
    #             return json.dumps({"error": error_message, "response": response.text})

    #     else:
    #         error_message = f"Failed to retrieve user information. Status code: {response.status_code}"
    #         return json.dumps({"error": error_message, "response": response.text})





    @staticmethod   
    def get_events():
        try:
            access_token = OpenAIFunctions.getEvents

            # Microsoft Graph API endpoint for retrieving events (meetings)
            api_url = "https://graph.microsoft.com/v1.0/me/events"

            headers = {
                "Authorization": f"Bearer {access_token}",
            }

            # Send a GET request to retrieve the user's events (meetings)
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                events = response.json().get("value", [])
                
                # Extract subject, start time, end time, and location for each event
                event_info = []
                for event in events:
                    subject = event.get("subject", "")
                    start_time = event.get("start", {}).get("dateTime", "")
                    end_time = event.get("end", {}).get("dateTime", "")
                    location = event.get("location", {}).get("displayName", "")
                    
                    event_info.append({
                        "subject": subject,
                        "start_time": start_time,
                        "end_time": end_time,
                        "location": location
                    })
                
                # Convert the event_info list to a JSON string
                event_info_json = json.dumps(event_info)
                
                return event_info_json
            else:
                error_message = f"Failed to retrieve events. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
                




    
    


FUNCTIONS_MAPPING = {
    "get_search_results": OpenAIFunctions.get_search_results,
    "get_current_weather": OpenAIFunctions.get_current_weather,
    "search_images": OpenAIFunctions.search_images,
    "service_now_ticket_creation":OpenAIFunctions.service_now_ticket_creation,
    "get_incident_status_by_number":OpenAIFunctions.get_incident_status_by_number,
    "get_recent_incidents_status":OpenAIFunctions.get_recent_incidents_status,
    "add_comment_to_incident":OpenAIFunctions.add_comment_to_incident,
    #"get_access_token":OpenAIFunctions.get_access_token,
    "send_email_via_graph_api":OpenAIFunctions.send_email_via_graph_api,
    "schedule_meeting_via_graph_api":OpenAIFunctions.schedule_meeting_via_graph_api,
    "cancel_meeting_by_name_via_graph_api":OpenAIFunctions.cancel_meeting_by_name_via_graph_api,
    "get_events":OpenAIFunctions.get_events,
    #"get_free_time_slots":OpenAIFunctions.get_free_time_slots,
    "find_meeting_times":OpenAIFunctions.find_meeting_times
}
