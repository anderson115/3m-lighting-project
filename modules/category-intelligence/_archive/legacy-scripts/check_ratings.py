import json

d=json.load(open('data/retailers/all_products_final_with_lowes.json'))
rated = [p for p in d if p.get('rating')]
reviewed = [p for p in d if p.get('reviews') and str(p.get('reviews')) != '0']

print(f'Total products: {len(d)}')
print(f'Products with ratings: {len(rated)} ({len(rated)/len(d)*100:.1f}%)')
print(f'Products with reviews: {len(reviewed)} ({len(reviewed)/len(d)*100:.1f}%)')

# Count negative reviews (1-2 stars)
negative = []
for p in rated:
    rating = p.get('rating')
    if rating and float(rating) <= 2.0:
        negative.append(p)

print(f'Products with 1-2 star ratings: {len(negative)}')
