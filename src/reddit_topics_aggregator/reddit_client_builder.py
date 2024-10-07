import os

from praw import Reddit

from .package_metadata import __title__, __version__


class RedditClientBuilder:
    def __init__(self):
        # Setting the default user agent
        self.user_agent = (
            os.getenv("REDDIT_USER_AGENT") or f"{__title__} / {__version__}"
        )
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.username = os.getenv("REDDIT_USERNAME")
        self.password = os.getenv("REDDIT_PASSWORD")

    def set_client_id(self, client_id):
        """Set client ID from method argument or environment variable."""
        self.client_id = client_id
        return self

    def set_client_secret(self, client_secret):
        """Set client secret from method argument or environment variable."""
        self.client_secret = client_secret
        return self

    def set_username(self, username):
        """Set Reddit username from method argument or environment variable."""
        self.username = username
        return self

    def set_password(self, password):
        """Set Reddit password from method argument or environment variable."""
        self.password = password
        return self

    def set_user_agent(self, user_agent):
        """Override the default user agent if needed."""
        self.user_agent = user_agent
        return self

    def build(self):
        """Build the praw.Reddit instance. Raise exception if any required argument is missing."""
        # Raise exception if required fields are not set
        missing_fields = []
        if not self.client_id:
            missing_fields.append("client_id")
        if not self.client_secret:
            missing_fields.append("client_secret")
        if not self.username:
            missing_fields.append("username")
        if not self.password:
            missing_fields.append("password")

        if missing_fields:
            raise ValueError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Create and return the Reddit client
        return Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.username,
            password=self.password,
            user_agent=self.user_agent,
        )

    @staticmethod
    def build_reddit_client_from_args(
        client_id=None,
        client_secret=None,
        username=None,
        password=None,
        user_agent=None,
    ):
        builder = RedditClientBuilder()

        if client_id:
            builder.set_client_id(client_id)
        if client_secret:
            builder.set_client_secret(client_secret)
        if username:
            builder.set_username(username)
        if password:
            builder.set_password(password)
        if user_agent:
            builder.set_user_agent(user_agent)

            # Build the Reddit client
        reddit_client = builder.build()
        return reddit_client
