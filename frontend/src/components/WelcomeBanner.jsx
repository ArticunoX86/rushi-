import React from 'react';
import { Rocket, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const WelcomeBanner = () => {
  return (
    <div className="glass-panel rounded-2xl p-8 relative overflow-hidden">
      {/* Decorative background glows */}
      <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 rounded-full bg-[rgba(139,92,246,0.15)] blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-64 h-64 rounded-full bg-[rgba(59,130,246,0.1)] blur-3xl pointer-events-none"></div>
      
      <div className="relative z-10 flex flex-col md:flex-row gap-8 items-center justify-between">
        <div className="max-w-md">
          <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <Rocket className="text-accent-primary" size={28} />
            Welcome to NexaVoice!
          </h2>
          <p className="text-muted leading-relaxed">
            Your AI calling agent is ready to go. Follow these quick steps to get your first automated campaign running.
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
          <Link to="/properties">
            <motion.div whileHover={{ scale: 1.05, y: -2 }} className="bg-[rgba(19,23,34,0.6)] border border-[rgba(255,255,255,0.08)] hover:border-[rgba(139,92,246,0.4)] transition-colors rounded-xl p-4 flex items-center gap-4 cursor-pointer group">
              <div className="w-8 h-8 rounded-full bg-[rgba(139,92,246,0.2)] text-accent-primary flex items-center justify-center font-bold text-sm">1</div>
              <div>
                <h4 className="text-white font-medium text-sm">Add Property</h4>
                <p className="text-muted text-xs">List your inventory</p>
              </div>
              <ArrowRight size={16} className="text-muted group-hover:text-white transition-colors ml-2" />
            </motion.div>
          </Link>
          
          <Link to="/leads">
            <motion.div whileHover={{ scale: 1.05, y: -2 }} className="bg-[rgba(19,23,34,0.6)] border border-[rgba(255,255,255,0.08)] hover:border-[rgba(59,130,246,0.4)] transition-colors rounded-xl p-4 flex items-center gap-4 cursor-pointer group">
              <div className="w-8 h-8 rounded-full bg-[rgba(59,130,246,0.2)] text-accent-secondary flex items-center justify-center font-bold text-sm">2</div>
              <div>
                <h4 className="text-white font-medium text-sm">Import Leads</h4>
                <p className="text-muted text-xs">Add people to call</p>
              </div>
              <ArrowRight size={16} className="text-muted group-hover:text-white transition-colors ml-2" />
            </motion.div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default WelcomeBanner;
