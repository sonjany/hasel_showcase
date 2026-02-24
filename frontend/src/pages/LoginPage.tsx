
export default function LoginPage({ onLogin }: { onLogin: () => void }) {
    return (
        <div className="relative flex items-center justify-center min-h-screen bg-black">
          {/*Hintergrundbild*/}  
          <div className="absolute inset-0 bg-[url('login-bg.jpg')] bg-cover bg-center opacity-40"/>

          <div className="relative z-10 w-full max-w-md p-8 border bg-black/80 border-white/10 backdrop-blur-xl">
            <h2 className="mb-6 text-3xl italic font-black text-center uppercase text-amber-600">
                Haselrodeo <span className="block text-sm text-white">Rider Access</span>
            </h2>

            <div className="space-y-4">
              <input
                type="email"
                placeholder="your e-mail address"
                className="w-full p-3 transition border outline-none bg-white/5 border-white/20 focus:border-amber-600"
            />
            <button
               onClick={onLogin}
               className="w-full py-3 font-bold text-black uppercase transition bg-amber-600 hover:bg-amber-500"
            >
                Register
            </button>
            </div>

            <p className="mt-6 text-[10px] text-center opacity-50 uppercase tracking-widest">
                Join the mud 2026
            </p>
          </div>
        </div>
    );
}