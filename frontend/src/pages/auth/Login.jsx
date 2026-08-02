import { useForm } from "react-hook-form";
import { Link, useNavigate, useLocation } from "react-router-dom";
import toast from "react-hot-toast";
import { useAuth } from "../../context/AuthContext";
import Input from "../../components/ui/Input";
import PasswordInput from "../../components/ui/PasswordInput";
import Button from "../../components/ui/Button";
import { extractErrorMessage } from "../../utils/format";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  async function onSubmit(values) {
    try {
      const user = await login(values.email, values.password);
      toast.success("Welcome back.");
      const from = location.state?.from?.pathname;
      navigate(from || (user?.role === "admin" ? "/admin/dashboard" : "/app/dashboard"), {
        replace: true,
      });
    } catch (err) {
      toast.error(extractErrorMessage(err));
    }
  }

  return (
    <div>
      <div className="mb-8">
        <p className="text-xs font-semibold uppercase tracking-wider text-ledger-500">Welcome back</p>
        <h2 className="mt-1.5 text-2xl font-display text-ink">Sign in to Ledger</h2>
        <p className="mt-1.5 text-sm text-ink-faint">Manage your subscription, invoices and payments.</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        <Input
          label="Email"
          type="email"
          autoComplete="email"
          placeholder="you@example.com"
          error={errors.email?.message}
          {...register("email", {
            required: "Email is required",
            pattern: { value: /^\S+@\S+\.\S+$/, message: "Enter a valid email" },
          })}
        />
        <PasswordInput
          label="Password"
          autoComplete="current-password"
          placeholder="••••••••"
          error={errors.password?.message}
          {...register("password", { required: "Password is required" })}
        />
        <Button type="submit" className="w-full" loading={isSubmitting}>
          Sign in
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-ink-faint">
        New to Ledger?{" "}
        <Link to="/register" className="font-medium text-ledger-600 hover:underline">
          Create an account
        </Link>
      </p>
    </div>
  );
}
