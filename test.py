from scrapers.app import ScraperApp
import time

start = time.perf_counter()

app = ScraperApp()
app.run()

end = time.perf_counter()
print(f"Elapsed: {end - start:.6f} s")