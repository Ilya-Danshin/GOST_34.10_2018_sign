from Crypto import Random


class RandomFileGenerator:
    @staticmethod
    def generate(name, size):
        rnd_bytes = Random.get_random_bytes(size)

        file = open(name, "wb")
        file.write(rnd_bytes)
        file.close()
