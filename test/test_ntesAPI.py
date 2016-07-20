import logging;logging.basicConfig(level=logging.INFO)
import ntesAPI

c1 = ntesAPI.generate_codes(3)
c2 = tuple(map(lambda self: '1'+self.zfill(6), c1))

result = ntesAPI.get_data(*c2)
