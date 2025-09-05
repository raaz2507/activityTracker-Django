ACTIVITY_SCHEMA = {
    "study":{
        "source":{"Books" : "", "Videos" : "", "Online Courses" : "", "Notes" : "", "Apps" : ""},
        "trigger":{"Interest" : "", "Exam Prep" : "", "Routine" : "", "Stress Relief" : ""},
        "extra":{},
        "color": "#ea580c",
        "icon": "Activity_icons/study_icon.svg"
    },
    "Sports / Gym":{
        "source":{"Outdoor" : "", "Gym Equipment" : "", "Coach/Trainer" : ""},
        "trigger":{"Fitness Goal" : "", "Stress Relief" : "", "Routine" : "", "Social Influence" : ""},
        "extra":{},
        "color": "#d97706",
    },
    "Movies / TV":{
        "source":{"Streaming Platform" : "", "TV" : "", "Cinema" : "", "Friends/Family" : ""},
        "trigger":{"Entertainment" : "", "Boredom" : "", "Social" : "", "Relaxation" : ""},
        "extra":{},
        "color": "#65a30d",
    },
    "Reading (Books/Comics)":{
        "source":{"Books" : "", "Comics" : "", "E-books" : "", "Online Articles" : ""},
        "trigger":{"Interest" : "", "Learning" : "", "Relaxation" : "", "Routine" : ""},
        "extra":{},
        "color": "#059669",
    },
    "Social Interaction":{
        "source":{"Friends" : "", "Family" : "", "Chat" : "", "Events" : "", "Online Groups" : ""},
        "trigger":{"Boredom" : "", "Friendship" : "", "Networking" : "", "Peer Influence" : ""},
        "extra":{},
        "color": "#0891b2",
    },
    "Gaming":{
        "source":{"Console" : "", "PC" : "", "Mobile" : "", "Online Multiplayer" : ""},
        "trigger":{"Entertainment" : "", "Stress Relief" : "", "Routine" : "", "Social" : ""},
        "extra":{},
        "color": "#ca8a04",
    },
    "Meditation / Yoga":{
        "source":{"App" : "", "Class" : "", "Outdoors" : "", "Self-Practice" : ""},
        "trigger":{"Stress Relief" : "", "Health" : "", "Routine" : "", "Self-Improvement" : ""},
        "extra":{},
        "color": "#db2777",
    },
    "Work / Coding":{
        "source":{"PC" : "", "Laptop" : "", "Notes" : "", "Online Tutorials" : ""},
        "trigger":{"Task Requirement" : "", "Interest" : "", "Learning" : "", "Challenge" : ""},
        "extra":{},
        "color": "#2563eb",
    },
    "Travel / Outing":{
        "source":{"Outdoors" : "", "Transport" : "", "Friends/Family" : ""},
        "trigger":{"Exploration" : "", "Social" : "", "Relaxation" : "", "Adventure" : ""},
        "extra":{},
        "color": "#9f57e0",
    },
    "Masturbation / Personal":{
        "source":{"Videos" : "", "Chat" : "", "Interaction" : "", "Device" : ""},
        "trigger":{"Boredom" : "", "Stress Relief" : "", "Routine" : "", "Curiosity" : "", "Long Gap" : ""},
        "extra":{"Times": ""},
        "color": "#fff",
    }
}
# {% for category, form in forms_dict.items %}
#   <h3>{{ category }}</h3>
#   <form method="post">
#     {% csrf_token %}
#     <input type="hidden" name="category" value="{{ category }}">
#     {{ form.start_time }}
#     {{ form.end_time }}
#     <br>
#     {% for field in form %}
#       {% if field.name != "start_time" and field.name != "end_time" and field.name != "activity" %}
#         <div>
#           <label>{{ field.label }}</label>
#           {{ field }}
#         </div>
#       {% endif %}
#     {% endfor %}
#     <button type="submit">Save {{ category }}</button>
#   </form>
# {% endfor %}