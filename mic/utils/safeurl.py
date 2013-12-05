"safe url"
import os

from zypp import Url


class SafeURL(str):
    "URL wrapper which won't show password out"
    def __new__(cls, urlstring):
        # sometimes we get unicode here, but zypp don't accept unicode string
        urlstring = str(urlstring)
        safe = Url(urlstring)
        safe.setUsername('')
        safe.setPassword('')

        safeurlstring = str(safe)
        if safeurlstring.startswith("file:/"):
            # zypp.Url converts file:///path/to/file to file:/path/to/file
            safeurlstring = "file://" + safeurlstring[len("file:"):]

        instance = super(SafeURL, cls).__new__(cls, safeurlstring)
        instance.url = Url(urlstring)
        return instance

    def join(self, *path):
        """
        Returns a new SafeURL with new path. Search part is removed since
        after join path is changed, keep the same search part is useless.
        """
        urlstring = self.without_search().full.rstrip('/')
        return SafeURL(os.path.join(urlstring, *path))

    @property
    def full(self):
        "Returns full url string with auth info"
        fullstring = self.url.asCompleteString()
        if fullstring.startswith("file:/"):
            fullstring = "file://" + fullstring[len("file:/"):]
        return fullstring

    def without_search(self):
        "Returns a SafeURL without search part"
        urlstring = self.full
        idx = urlstring.find('?')
        return self if idx == -1 else SafeURL(urlstring[:idx])

    @property
    def scheme(self):
        return self.url.getScheme()

    @property
    def user(self):
        return self.url.getUsername()

    @property
    def password(self):
        return self.url.getPassword()

    @property
    def host(self):
        return self.url.getHost()