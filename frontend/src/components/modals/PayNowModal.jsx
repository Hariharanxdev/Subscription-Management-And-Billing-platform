import { useForm, Controller } from "react-hook-form";
import { FiCreditCard, FiCheckCircle } from "react-icons/fi";
import Modal from "./Modal";
import Input from "../ui/Input";
import Select from "../ui/Select";
import Button from "../ui/Button";
import { PAYMENT_METHODS } from "../../constants";
import { formatCurrency } from "../../utils/format";

function formatCardNumber(value) {
  return value
    .replace(/\D/g, "")
    .slice(0, 16)
    .replace(/(.{4})/g, "$1 ")
    .trim();
}

function formatExpiry(value) {
  const digits = value.replace(/\D/g, "").slice(0, 4);
  if (digits.length <= 2) return digits;
  return `${digits.slice(0, 2)}/${digits.slice(2)}`;
}

export default function PayNowModal({ open, onClose, subscription, onSubmit, submitting, success }) {
  const {
    register,
    handleSubmit,
    control,
    reset,
    watch,
    formState: { errors },
  } = useForm({
    defaultValues: { paymentMethod: "card", cardNumber: "", expiry: "", cvv: "", cardName: "" },
  });

  const method = watch("paymentMethod");

  function handleClose() {
    reset();
    onClose();
  }

  function submit(values) {
    onSubmit(values.paymentMethod);
  }

  return (
    <Modal open={open} onClose={handleClose} title="Pay for subscription" size="md">
      {success ? (
        <div className="flex flex-col items-center gap-3 py-6 text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-ledger-50 text-ledger-500">
            <FiCheckCircle size={28} />
          </div>
          <p className="font-display text-lg text-ink">Payment successful</p>
          <p className="text-sm text-ink-faint">An invoice has been generated automatically.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit(submit)} className="space-y-4" noValidate>
          {subscription && (
            <div className="leader-row rounded-lg bg-paper-dim/60 px-3.5 py-3 text-sm">
              <span className="text-ink-soft">{subscription.plan.plan_name}</span>
              <span className="leader-fill" />
              <span className="tabular font-medium text-ink">
                {formatCurrency(subscription.plan.price)}
              </span>
            </div>
          )}

          <Controller
            control={control}
            name="paymentMethod"
            render={({ field }) => (
              <Select label="Payment method" options={PAYMENT_METHODS} {...field} />
            )}
          />

          {method === "card" && (
            <div className="space-y-4 rounded-xl border border-line p-4">
              <Input
                label="Card number"
                placeholder="4242 4242 4242 4242"
                inputMode="numeric"
                error={errors.cardNumber?.message}
                {...register("cardNumber", {
                  required: "Card number is required",
                  minLength: { value: 19, message: "Enter a 16-digit card number" },
                  onChange: (e) => {
                    e.target.value = formatCardNumber(e.target.value);
                  },
                })}
              />
              <div className="grid grid-cols-2 gap-3">
                <Input
                  label="Expiry"
                  placeholder="MM/YY"
                  inputMode="numeric"
                  error={errors.expiry?.message}
                  {...register("expiry", {
                    required: "Required",
                    minLength: { value: 5, message: "MM/YY" },
                    onChange: (e) => {
                      e.target.value = formatExpiry(e.target.value);
                    },
                  })}
                />
                <Input
                  label="CVV"
                  placeholder="123"
                  inputMode="numeric"
                  type="password"
                  error={errors.cvv?.message}
                  {...register("cvv", {
                    required: "Required",
                    minLength: { value: 3, message: "3 digits" },
                    maxLength: { value: 4, message: "Max 4 digits" },
                  })}
                />
              </div>
              <Input
                label="Name on card"
                placeholder="As shown on card"
                error={errors.cardName?.message}
                {...register("cardName", { required: "Required" })}
              />
            </div>
          )}

          {method === "upi" && (
            <Input label="UPI ID" placeholder="yourname@bank" {...register("upiId")} />
          )}

          <Button type="submit" className="w-full" loading={submitting} icon={<FiCreditCard size={15} />}>
            Pay {subscription ? formatCurrency(subscription.plan.price) : ""}
          </Button>
          <p className="text-center text-[11px] text-ink-faint">
            This is a simulated payment for demo purposes — no real card is charged.
          </p>
        </form>
      )}
    </Modal>
  );
}
