// frontend/src/screens/Portfolio/PortfolioScreen.tsx
import React, { useEffect } from 'react';
import { ScrollView, View, Text, TouchableOpacity, RefreshControl } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';
import { Svg, Path } from 'react-native-svg';
import { useWealthStore } from '../../store/useWealthStore';

export default function PortfolioScreen() {
  const insets = useSafeAreaInsets();
  const { snapshot, isLoading, fetchSnapshot } = useWealthStore();

  useEffect(() => {
    fetchSnapshot();
  }, []);

  const HealthSpectrum = () => (
    <View className="items-center space-y-8 my-8">
      <View className="flex-row items-end gap-2 h-32 mb-4">
        {[40, 60, 75].map((h, i) => (
          <View key={i} style={{ height: `${h}%`, width: 16 }} className="bg-white/10 rounded-t-sm" />
        ))}
        {[85, 95, 100, 90].map((h, i) => (
          <View key={i+3} style={{ height: `${h}%`, width: 24 }} className="bg-accent rounded-t-sm" />
        ))}
        {[40, 40].map((h, i) => (
          <View key={i+7} style={{ height: `${h}%`, width: 16 }} className="bg-white/5 border border-dashed border-white/20 rounded-t-sm" />
        ))}
      </View>
      <View className="bg-primary/40 px-8 py-3 rounded-2xl border border-borderWhite flex-row items-baseline">
        <Text className="text-textPrimary text-6xl font-bold tracking-[-0.5]er">{snapshot?.portfolio_health_score || 0}</Text>
        <Text className="text-textPrimary opacity-40 text-base font-medium ml-2">/100</Text>
      </View>
    </View>
  );

  return (
    <View className="flex-1 bg-primary">
      {/* Header */}
      <View 
        className="px-6 py-4 flex-row justify-between items-center border-b border-borderWhite bg-primary/80"
        style={{ paddingTop: insets.top }}
      >
        <TouchableOpacity>
          <MaterialIcons name="account-balance-wallet" size={24} color="#00E5C0" />
        </TouchableOpacity>
        <Text className="font-bold text-lg tracking-[-0.5]er text-textPrimary uppercase">PORTFOLIO</Text>
        <TouchableOpacity>
          <Ionicons name="notifications-outline" size={24} color="#00E5C0" />
        </TouchableOpacity>
      </View>

      <ScrollView 
        className="flex-1" 
        contentContainerClassName="px-6 pb-24"
        refreshControl={<RefreshControl refreshing={isLoading} onRefresh={fetchSnapshot} tintColor="#00E5C0" />}
      >
        {/* System Status */}
        <View className="flex-row justify-between items-center border-b border-borderWhite pb-4 mt-8">
          <Text className="text-textPrimary opacity-40 text-[10px] uppercase tracking-widest font-bold">System Status</Text>
          <View className="border border-accent/30 px-3 py-1 rounded-full bg-accent/10">
            <Text className="text-accent text-[10px] uppercase tracking-widest font-bold">Optimal</Text>
          </View>
        </View>

        <HealthSpectrum />

        <Text className="text-textPrimary opacity-60 text-center leading-relaxed text-sm mb-12">
          Portfolio composition is stable. Structural adjustments recommended in liquidity buffers to mitigate tail risk.
        </Text>

        {/* Intelligence Grid */}
        <View className="mb-12">
          <View className="flex-row justify-between items-end border-b border-borderWhite pb-4 mb-6">
            <Text className="text-textPrimary opacity-40 text-[10px] uppercase tracking-widest font-bold">Intelligence Grid</Text>
            <Text className="text-textPrimary opacity-20 text-[10px] font-bold">04 FACTORS</Text>
          </View>

          {/* Grid Layout (Mocked as Flex columns/rows for simplicity in RN) */}
          <View className="flex-col gap-4">
            {/* Return Quality */}
            <View className="bg-surface border border-borderWhite p-6 rounded-3xl relative overflow-hidden">
               <View className="flex-row justify-between items-start mb-4">
                 <Text className="text-textPrimary opacity-60 text-[10px] uppercase tracking-[2] font-bold">Return Quality</Text>
                 <View className="px-2 py-1 bg-accent/10 rounded border border-accent/30">
                   <Text className="text-accent text-[10px] uppercase tracking-widest font-bold">Alpha</Text>
                 </View>
               </View>
               <View className="flex-row items-baseline mb-4">
                 <Text className="text-textPrimary text-6xl font-bold tracking-[-0.5]er">10</Text>
                 <Text className="text-textPrimary opacity-40 text-base font-medium ml-2">/10</Text>
               </View>
               <View className="h-0.5 bg-white/10 w-full relative">
                 <View className="absolute inset-y-0 left-0 w-full bg-accent h-full shadow-lg" />
               </View>
               <Text className="text-textPrimary opacity-40 text-[11px] mt-6 uppercase tracking-wide">Exceptional yield generation against benchmarks.</Text>
            </View>

            <View className="flex-row gap-4">
              {/* Diversification */}
              <View className="flex-1 bg-surface border border-borderWhite p-5 rounded-2xl">
                <Text className="text-textPrimary opacity-60 text-[10px] uppercase tracking-[2] font-bold mb-4">Diversification</Text>
                <View className="flex-row items-end justify-between">
                   <View className="flex-row items-baseline">
                     <Text className="text-textPrimary text-4xl font-bold tracking-[-0.5]er">7</Text>
                     <Text className="text-textPrimary opacity-40 text-xs font-medium ml-1">/10</Text>
                   </View>
                   <Svg width="40" height="20" viewBox="0 0 100 30">
                     <Path d="M0,30 Q25,0 50,20 T100,5" fill="none" stroke="#00E5C0" strokeWidth="4" />
                   </Svg>
                </View>
              </View>

              {/* Alignment */}
              <View className="flex-1 bg-surface border border-borderWhite p-5 rounded-2xl">
                <Text className="text-textPrimary opacity-60 text-[10px] uppercase tracking-[2] font-bold mb-4">Alignment</Text>
                <View className="flex-row items-end justify-between">
                   <View className="flex-row items-baseline">
                     <Text className="text-textPrimary text-4xl font-bold tracking-[-0.5]er">6</Text>
                     <Text className="text-textPrimary opacity-40 text-xs font-medium ml-1">/10</Text>
                   </View>
                   <View className="flex-row gap-0.5 items-end h-6">
                     <View className="w-1 bg-white/40 h-[40%] rounded-sm" />
                     <View className="w-1 bg-white/60 h-[60%] rounded-sm" />
                     <View className="w-1 bg-white h-[80%] rounded-sm" />
                     <View className="w-1 border border-dashed border-white/20 h-[100%] rounded-sm" />
                   </View>
                </View>
              </View>
            </View>

            {/* Emergency Buffer */}
            <TouchableOpacity className="bg-danger/5 border border-danger/20 p-5 rounded-2xl flex-row items-center justify-between">
               <View className="flex-row items-center gap-4">
                 <View className="bg-danger/10 w-12 h-12 rounded-xl border border-danger/20 items-center justify-center">
                   <Text className="text-danger text-2xl font-bold">4</Text>
                 </View>
                 <View>
                   <View className="flex-row items-center gap-1 mb-0.5">
                     <Text className="text-danger text-[10px] uppercase tracking-widest font-bold">Emergency Buffer</Text>
                     <Ionicons name="warning-outline" size={10} color="#E63946" />
                   </View>
                   <Text className="text-textPrimary opacity-50 text-[10px]">Liquidity below 6-month threshold.</Text>
                 </View>
               </View>
               <TouchableOpacity 
                 className="bg-white/10 px-4 py-2 rounded-full border border-white/20"
                 onPress={() => alert("Quick Transfer Initiated\n\nMoving ₹20,000 from Savings to Emergency Liquid Fund.")}
               >
                 <Text className="text-textPrimary text-[10px] uppercase tracking-[2] font-bold">Fix</Text>
               </TouchableOpacity>
               </TouchableOpacity>
          </View>
        </View>

        {/* Asset Allocation */}
        <View className="mb-8">
           <View className="flex-row justify-between items-end border-b border-borderWhite pb-4 mb-6">
            <Text className="text-textPrimary opacity-40 text-[12px] uppercase tracking-widest font-bold">Asset Allocation</Text>
          </View>
          
          {snapshot?.investments.map((inv) => (
            <TouchableOpacity key={inv.id} className="bg-surface border border-borderWhite rounded-3xl p-6 mb-3 flex-row justify-between items-center">
              <View className="flex-row items-center gap-4">
                <View className="w-12 h-12 bg-white/5 rounded-xl border border-borderWhite items-center justify-center">
                  <MaterialIcons name="trending-up" size={24} color="#F2EDE4" />
                </View>
                <View>
                  <Text className="text-textPrimary text-sm uppercase tracking-widest font-bold">{inv.scheme_name}</Text>
                  <Text className="text-textPrimary opacity-40 text-[10px] uppercase tracking-wider font-bold">{inv.account_type}</Text>
                </View>
              </View>
              <View className="items-end">
                <Text className="text-textPrimary opacity-80 text-2xl font-bold tracking-[-0.5]">₹{inv.current_value.toLocaleString()}</Text>
                {inv.returns_xirr && <Text className="text-accent text-[10px] font-bold">+{inv.returns_xirr}% XIRR</Text>}
              </View>
            </TouchableOpacity>
          ))}

          {snapshot?.assets.map((asset) => (
            <TouchableOpacity key={asset.id} className="bg-surface border border-borderWhite rounded-3xl p-6 mb-3 flex-row justify-between items-center">
              <View className="flex-row items-center gap-4">
                <View className="w-12 h-12 bg-white/5 rounded-xl border border-borderWhite items-center justify-center">
                  <MaterialIcons name="account-balance" size={24} color="#F2EDE4" />
                </View>
                <View>
                  <Text className="text-textPrimary text-sm uppercase tracking-widest font-bold">{asset.name}</Text>
                  <Text className="text-textPrimary opacity-40 text-[10px] uppercase tracking-wider font-bold">{asset.asset_type}</Text>
                </View>
              </View>
              <View className="items-end">
                <Text className="text-textPrimary opacity-80 text-2xl font-bold tracking-[-0.5]">₹{asset.current_value.toLocaleString()}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </View>
  );
}
