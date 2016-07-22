import logging;logging.basicConfig(level=logging.INFO)
import ntesDS

c1 = ntesDS.generate_codes(3)
c2 = tuple(map(lambda self: '1'+self.zfill(6), c1))

result = ntesDS.get_data(*c2)
