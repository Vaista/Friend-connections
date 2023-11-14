from neomodel import config, StructuredNode, StringProperty, Relationship, StructuredRel, DateTimeProperty, db
from datetime import datetime
import pytz

from app.config import DATABASE_URL


config.DATABASE_URL = DATABASE_URL


class FriendRequest(StructuredRel):
    """Custom relationship model for friend requests"""
    # You can add additional properties to the relationship if needed
    created_at = DateTimeProperty(default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))


class FriendRel(StructuredRel):
    """Custom relationship model for friend requests"""
    # You can add additional properties to the relationship if needed
    created_at = DateTimeProperty(default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))


class User(StructuredNode):
    """Class to model a user"""
    email = StringProperty(unique_index=True, required=True)
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    friend_requests = Relationship('User', 'FRIEND_REQUEST', model=FriendRequest)
    friends = Relationship('User', 'FRIEND', model=FriendRel)

    def send_friend_request(self, other_user):
        """Function to send friend requests"""
        if not self.friends.is_connected(other_user) and not self.friend_requests.is_connected(other_user):
            self.friend_requests.connect(other_user)

    def get_received_friend_requests(self):
        """Returns the received friend requests"""
        query = "MATCH (p1:User) -[r:FRIEND_REQUEST]-> (p2:User) WHERE p2.email = $user_email RETURN p1;"
        results, columns = db.cypher_query(query, params={'user_email': self.email}, resolve_objects=True)
        return results

    def get_sent_friend_requests(self):
        """Returns the friend requests sent by the user"""
        query = "MATCH (p1:User) -[r:FRIEND_REQUEST]-> (p2:User) WHERE p1.email = $user_email RETURN p2;"
        results, columns = db.cypher_query(query, params={'user_email': self.email}, resolve_objects=True)
        return results

    def delete_friend_request(self, other_user):
        """Deletes a Friend Request connection between users"""
        self.friend_requests.disconnect(other_user)
        other_user.friend_requests.disconnect(self)

    def make_friend(self, other_user):
        """Remove the friend request relation and create friend relation between the users"""
        self.friend_requests.disconnect(other_user)
        other_user.friend_requests.disconnect(self)
        self.friends.connect(other_user)
        other_user.friends.connect(self)

    def remove_friend(self, other_user):
        """Removes the friend relation between the users"""
        if self.friends.is_connected(other_user):
            self.friends.disconnect(other_user)
            other_user.friends.disconnect(self)

    def get_friend_list(self):
        """Returns the friend list of the user"""
        query = "MATCH (p1:User) -[r:FRIEND]-> (p2:User) WHERE p1.email = $user_email RETURN p2;"
        results, columns = db.cypher_query(query, params={'user_email': self.email}, resolve_objects=True)
        return results
