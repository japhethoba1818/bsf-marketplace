# BSF Marketplace

A web marketplace connecting BSF members with businesses and service providers within their community — built for the BSF Interim Task Team, South Africa.

**"NOW OR NEVER"**
*Bokamoso bja ekonomi ya rena ke boipereki.*

## What it does

- Business owners register their business (with photos, category, location, pricing) and get approved for listing
- BSF members search the marketplace by category, location, and price to find a service
- Members request a quote directly from a business's profile
- Business owners respond to quote requests from their own Provider Dashboard
- Members follow up via WhatsApp using the pre-filled contact link

## Tech stack

- **Frontend/App**: Streamlit (Python)
- **Database & Auth**: Supabase (PostgreSQL + Auth + Storage)
- **Hosting**: Render

## Local setup (Codespaces)

source .venv/bin/activate
streamlit run app.py

Requires a `.streamlit/secrets.toml` (gitignored — not committed) with your Supabase project URL and anon key.

## Project structure

app.py                          # Landing page
pages/
  1_Find_a_Service.py           # Marketplace search
  2_Register_My_Business.py     # Business registration (requires login)
  _Business_Profile.py          # Business profile view (reached via search)
  _Request_Quote.py             # Quote request form (reached via profile)
  5_Provider_Dashboard.py       # Provider dashboard (requires login)
  6_Sign_In.py                  # Auth
lib/
  db.py                         # Supabase client
  auth.py                       # Auth helpers

## Database schema

- `businesses` — registered businesses, owned by an authenticated user, approval-gated (`status`: pending/approved)
- `quote_requests` — member requests submitted against a business
- `quotes` — provider responses to a quote request

Row Level Security (RLS) restricts quote data to the owning business's authenticated user.

## Status

Phases 0–13 complete: full registration → search → quote request → provider response flow, authentication, RLS security hardening, mobile-friendly UI, end-to-end tested.

Currently deploying to Render (Phase 14).

## Known deferred items

- Storage bucket uploads aren't ownership-restricted at the DB level (low risk — no personal data exposure)
- Sidebar still shows Business Profile / Request Quote as direct links (cosmetic, low priority)
- New business approval is manual via Supabase dashboard (fine at current scale; admin approval page planned once past ~10 businesses)
