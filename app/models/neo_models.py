from neomodel import config, StructuredNode, StringProperty, RelationshipTo, Relationship

from app.config import DATABASE_URL


config.DATABASE_URL = DATABASE_URL


class User(StructuredNode):
    """Class to model a user"""
    email = StringProperty(unique_index=True, required=True)
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    friend_requests_sent = RelationshipTo('User', 'FRIEND_REQUEST')
    friends = Relationship('User', 'FRIEND')

    def send_friend_request(self, other_user):
        """Function to send friend requests"""
        if not self.friends.is_connected(other_user) and not self.friend_requests_sent.is_connected(other_user):
            self.friend_requests_sent.connect(other_user)

    def accept_friend_request(self, other_user):
        """Function to accept friend requests"""
        if self.friend_requests_sent.is_connected(other_user):
            self.friend_requests_sent.disconnect(other_user)
            self.friends.connect(other_user)

    def get_sent_friend_requests(self):
        """Function to display sent friend requests"""
        return self.friend_requests_sent.all()

    def get_received_friend_requests(self):
        """Function to display received friend requests"""
        # Find all users who sent a friend request to the current user
        return User.nodes.filter(friend_requests_sent__from_user=self)
