from flask-newsmarkr import db
from datetime import datetime

# profile constants
POLITICAL_SPECTRUM = {
    'far_left': 'Far-left',
    'centre_left': 'Centre-left',
    'centre': 'Centre',
    'centre_right': 'Centre-right',
    'far_right': 'Far-right'
}

POLITICAL_PARTIES = {
    'conservative_party': 'Conservative and Unionist Party',
    'labour_party': 'Labour Party',
    'scottish_national_party': 'Scottish National Party',
    'liberal_democrats': 'Liberal Democrats',
    'democratic_unionist_party': 'Democratic Unionist Party',
    'sinn_féin': 'Sinn Féin',
    'plaid_cymru_party_of_wales': 'Plaid Cymru - Party of Wales',
    'green_party': 'Green Party',
    'social_democratic_and_labour_party': 'Social Democratic and Labour Party',
    'ulster_unionist_party': 'Ulster Unionist Party',
    'uk_independence_party': 'UK Independence Party',
    'alliance_party_of_northern_ireland': 'Alliance Party of Northern Ireland',
    'scottish_green_party': 'Scottish Green Party',
    'green_party_in_northern_ireland': 'Green Party in Northern Ireland',
    'traditional_unionist_voice': 'Traditional Unionist Voice',
    'people_before_profit_alliance': 'People Before Profit Alliance'
}

FAVOURITE_NEWS_WEBSITES = {
    'bbc_news': 'BBC News',
    'the_guardian': 'The Guardian',
    'the_telegraph': 'The Telegraph',
    'daily_mail': 'Daily Mail',
    'the_independent': 'The Independent',
    'daily_mirror': 'Daily Mirror',
    'the_sun': 'The Sun',
    'daily_express': 'Daily Express',
    'metro': 'Metro',
    'channel_4_news': 'Channel 4 News',
    'independent_ie': 'Independent.ie',
    'the_huffington_post': 'The Huffington Post',
    'evening_standard': 'Evening Standard',
    'the_irish_times': 'The Irish Times',
    'manchester_evening_news': 'Manchester Evening News (MEN)',
    'the_conversation': 'The Conversation',
    'pinknews': 'PinkNews',
    'wired_uk': 'Wired UK',
    'the_daily_record': 'The Daily Record',
    'wales_online': 'Wales Online',
    'the_poke': 'The Poke',
    'birmingham_mail': 'Birmingham Mail',
    'belfast_telegraph': 'Belfast Telegraph',
    'the_scotsman': 'The Scotsman',
    'the_daily_mash': 'The Daily Mash',
    'the_week_uk': 'The Week UK',
    'herald_scotland': 'Herald Scotland',
    'breaking_news_ie': 'BreakingNews.ie',
    'the_scottish_sun': 'The Scottish Sun',
    'the_argus': 'The Argus',
    'cambridge_news': 'Cambridge News',
    'the_evening_times': 'The Evening Times',
    'the_york_press': 'The York Press',
    'the_northern_echo': 'The Northern Echo',
    'the_bolton_news': 'The Bolton News',
    'the_news_portsmouth': 'The News, Portsmouth',
    'grimsby_telegraph': 'Grimsby Telegraph',
    'politics_co_uk': 'Politics.co.uk',
    'belfast_live': 'Belfast Live',
    'the_voice': 'The Voice',
    'sky_news': 'Sky News',
    'positive_news': 'Positive News',
    'the_scarborough_news': 'The Scarborough News',
    'deadline_news': 'Deadline News',
    'newsnet_scot': 'Newsnet.scot',
    'larne_times': 'Larne Times',
    'coleraine_times': 'Coleraine Times',
    'the_church_of_england_newspaper': 'The Church of England Newspaper',
    'scottish_field': 'Scottish Field',
    'daily_echo': 'Daily Echo',
    'necn': 'NECN'
}

NEWS_WEBSITE_LINKS = {
    'bbc_news': 'http://www.bbc.co.uk/news',
    'the_guardian': 'https://www.theguardian.com/uk',
    'the_telegraph': 'https://www.telegraph.co.uk/',
    'daily_mail': 'http://www.dailymail.co.uk/home/index.html',
    'the_independent': 'https://www.independent.co.uk/',
    'daily_mirror': 'https://www.mirror.co.uk/',
    'the_sun': 'https://www.thesun.co.uk/',
    'daily_express': 'https://www.express.co.uk/',
    'metro': 'http://metro.co.uk/',
    'channel_4_news': 'https://www.channel4.com/news/',
    'independent_ie': 'https://www.independent.ie/',
    'the_huffington_post': 'https://www.huffingtonpost.co.uk/',
    'evening_standard': 'https://www.standard.co.uk/',
    'the_irish_times': 'https://www.irishtimes.com/',
    'manchester_evening_news': 'https://www.manchestereveningnews.co.uk/',
    'the_conversation': 'http://theconversation.com/uk',
    'pinknews': 'https://www.pinknews.co.uk/home/',
    'wired_uk': 'http://www.wired.co.uk/',
    'the_daily_record': 'https://www.dailyrecord.co.uk/',
    'wales_online': 'https://www.walesonline.co.uk/',
    'the_poke': 'https://www.thepoke.co.uk/',
    'birmingham_mail': 'https://www.birminghammail.co.uk/',
    'belfast_telegraph': 'https://www.belfasttelegraph.co.uk/',
    'the_scotsman': 'https://www.scotsman.com/',
    'the_daily_mash': 'http://www.thedailymash.co.uk/',
    'the_week_uk': 'http://www.theweek.co.uk/',
    'herald_scotland': 'http://www.heraldscotland.com/',
    'breaking_news_ie': 'https://www.breakingnews.ie/',
    'the_scottish_sun': 'https://www.thescottishsun.co.uk/',
    'the_argus': 'http://www.theargus.co.uk/',
    'cambridge_news': 'https://www.cambridge-news.co.uk/',
    'the_evening_times': 'http://www.eveningtimes.co.uk/',
    'the_york_press': 'http://www.yorkpress.co.uk/',
    'the_northern_echo': 'http://www.thenorthernecho.co.uk/',
    'the_bolton_news': 'http://www.theboltonnews.co.uk/',
    'the_news_portsmouth': 'https://www.portsmouth.co.uk/',
    'grimsby_telegraph': 'https://www.grimsbytelegraph.co.uk/',
    'politics_co_uk': 'http://www.politics.co.uk/',
    'belfast_live': 'https://www.belfastlive.co.uk/',
    'the_voice': 'http://www.voice-online.co.uk/',
    'sky_news': 'https://news.sky.com/uk',
    'positive_news': 'https://www.positive.news/',
    'the_scarborough_news': 'https://www.thescarboroughnews.co.uk/',
    'deadline_news': 'http://www.deadlinenews.co.uk/',
    'newsnet_scot': 'http://newsnet.scot/',
    'larne_times': 'https://www.larnetimes.co.uk/',
    'coleraine_times': 'https://www.colerainetimes.co.uk/',
    'the_church_of_england_newspaper': 'http://www.churchnewspaper.com/',
    'scottish_field': 'https://www.scottishfield.co.uk/',
    'daily_echo': 'http://www.dailyecho.co.uk/',
    'necn': 'https://www.necn.com/'
}


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.String(256))
    accepted_on = db.Column(db.Date)

    def __init__(self, user_id, friend_id, created_on, accepted_on):
        self.user_id = user_id
        self.friend_id = friend_id
        self.created_on = created_on
        self.accepted_on = accepted_on

    def __repr__(self):
        return '<Friends %r>' % self.user_id


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_accepted = db.Column(db.Boolean)
    friend_accepted = db.Column(db.Boolean)
    user_ignored = db.Column(db.Boolean)
    friend_ignored = db.Column(db.Boolean)
    created_on = db.Column(db.Date)
    accepted_on = db.Column(db.Date)

    def __init__(self, user_id, friend_id, user_accepted, friend_accepted, user_ignored, friend_ignored, created_on, accepted_on):
        self.user_id = user_id
        self.friend_id = friend_id
        self.user_accepted = user_accepted
        self.friend_accepted = friend_accepted
        self.user_ignored = user_ignored
        self.friend_ignored = friend_ignored
        self.created_on = created_on
        self.accepted_on = accepted_on

    def __repr__(self):
        return '<FriendRequest %r>' % self.user_id


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    birthday = db.Column(db.Date)
    political_spectrum = db.Column(db.String(256))
    political_party = db.Column(db.String(256))
    # accepted as array -> convert in init
    favourite_news_websites = db.Column(db.Text())
    allow_location_detection = db.Column(db.Boolean)
    location = db.Column(db.String(256))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self, user_id, birthday, political_spectrum, political_party, favourite_news_websites, allow_location_detection, location, lat, lon):
        self.user_id = user_id
        self.birthday = birthday
        self.political_spectrum = political_spectrum
        self.political_party = political_party
        # convert list to comma-separated string
        self.favourite_news_websites = ",".join(favourite_news_websites)
        self.allow_location_detection = allow_location_detection
        self.location = location
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<Profile %r>' % self.user_id
