import ntesAPI

c1 = ntesAPI.generate_codes(3)
c2 = tuple(map(lambda self: '1'+self.zfill(6), c1))

urls = tuple(map(lambda self: ntesAPI.make_ntes_url(self), c2))
result = ntesAPI.get_urls(*urls)