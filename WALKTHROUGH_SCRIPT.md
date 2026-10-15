# 10-minute walkthrough script

**0:00–1:00 | Problem**  
“This tool monitors weekly freight cost per tonne-kilometre by route. It compares each route against its own previous eight observed weeks and other routes of the same route type in the same week.”

**1:00–3:00 | Data and calculation**  
“I use the provided route_type and assign every shipment to the Monday of its week. Weekly cost is total freight cost divided by total quantity-times-distance. The history baseline only uses prior weeks, so there is no look-ahead.”

**3:00–5:00 | Comparison logic**  
“The peer baseline averages other routes of the same Short/Medium/Long type in that week, excluding the current route. The brief doesn’t specify a numeric threshold, so I documented +20% as an explicit policy assumption. A flag triggers when either available comparison reaches that threshold.”

**5:00–7:00 | Evidence grounding**  
“When a route is flagged, I validate context notes by route, date window, and whether the note actually describes a cost increase. Notes saying costs were unaffected, routes outside the dataset, improved conditions, or no disruption are not accepted as justification. If no valid note matches, the row is marked Yes for human review.”

**7:00–8:00 | Output and dashboard**  
“Each output row includes the route, Monday week date, cost, both comparisons, verdict, matched note ID, and reason. The Streamlit UI filters routes/verdicts, plots cost trends, and downloads CSV.”

**8:00–9:00 | Validation**  
“I ran four automated tests and ran the full pipeline three times. The output hashes match, showing the calculations and verdicts are deterministic.”

**9:00–10:00 | Cost and limitations**  
“This version makes zero LLM calls, so token usage and LLM cost are zero. This avoids invented explanations and makes the verdicts auditable. The trade-off is that natural-language Q&A and LLM-generated explanations are not implemented. The +20% threshold is an explicit assumption and should be tuned with business owners.”
