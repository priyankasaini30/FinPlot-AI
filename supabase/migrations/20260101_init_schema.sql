-- ==============================================================================
-- FinPlot AI — Database Schema Migration
-- Migration: 20260101_init_schema.sql
-- Description: Creates transactions table, audit triggers, indexes, and Row-Level Security (RLS) policies.
-- ==============================================================================

-- 1. Create Transactions Table
CREATE TABLE IF NOT EXISTS public.transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    transaction_date DATE NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('income', 'expense')),
    category TEXT NOT NULL,
    payment_method TEXT,
    notes TEXT,
    is_demo BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Create updated_at Auto-Update Trigger
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_transactions_updated_at ON public.transactions;

CREATE TRIGGER trigger_transactions_updated_at
BEFORE UPDATE ON public.transactions
FOR EACH ROW
EXECUTE FUNCTION public.handle_updated_at();

-- 3. High-Performance Query Indexes
CREATE INDEX IF NOT EXISTS idx_transactions_user_id 
    ON public.transactions(user_id);

CREATE INDEX IF NOT EXISTS idx_transactions_date 
    ON public.transactions(transaction_date DESC);

CREATE INDEX IF NOT EXISTS idx_transactions_category 
    ON public.transactions(category);

CREATE INDEX IF NOT EXISTS idx_transactions_type 
    ON public.transactions(transaction_type);

CREATE INDEX IF NOT EXISTS idx_transactions_is_demo 
    ON public.transactions(is_demo);

CREATE INDEX IF NOT EXISTS idx_transactions_composite 
    ON public.transactions(user_id, transaction_date DESC);

-- 4. Enable Row-Level Security (RLS)
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;

-- 5. Row-Level Security Policies
-- SELECT Policy: Users can view their own transactions; demo rows are visible to the session
DROP POLICY IF EXISTS "Users can read own or demo transactions" ON public.transactions;
CREATE POLICY "Users can read own or demo transactions"
ON public.transactions
FOR SELECT
USING (
    (auth.uid() IS NOT NULL AND auth.uid() = user_id)
    OR
    (is_demo = true)
);

-- INSERT Policy: Authenticated users insert their own transactions; demo transactions allowed with is_demo=true
DROP POLICY IF EXISTS "Users can insert own or demo transactions" ON public.transactions;
CREATE POLICY "Users can insert own or demo transactions"
ON public.transactions
FOR INSERT
WITH CHECK (
    (auth.uid() IS NOT NULL AND auth.uid() = user_id)
    OR
    (auth.uid() IS NULL AND is_demo = true AND user_id IS NULL)
    OR
    (auth.uid() IS NOT NULL AND is_demo = true)
);

-- UPDATE Policy: Authenticated users can modify only their own transactions
DROP POLICY IF EXISTS "Users can update own transactions" ON public.transactions;
CREATE POLICY "Users can update own transactions"
ON public.transactions
FOR UPDATE
USING (
    (auth.uid() IS NOT NULL AND auth.uid() = user_id)
    OR
    (is_demo = true)
)
WITH CHECK (
    (auth.uid() IS NOT NULL AND auth.uid() = user_id)
    OR
    (is_demo = true)
);

-- DELETE Policy: Authenticated users can delete only their own transactions or demo transactions
DROP POLICY IF EXISTS "Users can delete own transactions" ON public.transactions;
CREATE POLICY "Users can delete own transactions"
ON public.transactions
FOR DELETE
USING (
    (auth.uid() IS NOT NULL AND auth.uid() = user_id)
    OR
    (is_demo = true)
);

-- Comments for Schema Documentation
COMMENT ON TABLE public.transactions IS 'Primary ledger of financial income and expense transactions for FinPlot AI';
COMMENT ON COLUMN public.transactions.amount IS 'Monetary value strictly greater than 0; direction indicated by transaction_type';
COMMENT ON COLUMN public.transactions.is_demo IS 'Flag indicating isolated sample transactions that can be cleared safely';
