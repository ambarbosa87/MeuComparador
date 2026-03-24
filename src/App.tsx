/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { Plus, Trash2, Calculator, ShoppingCart, Info, CheckCircle2, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

type UnitType = 'g' | 'kg' | 'ml' | 'l' | 'un';

interface Item {
  id: string;
  name: string;
  price: number;
  quantity: number;
  unit: UnitType;
}

const UNIT_LABELS: Record<UnitType, string> = {
  g: 'Gramas (g)',
  kg: 'Quilos (kg)',
  ml: 'Mililitros (ml)',
  l: 'Litros (l)',
  un: 'Unidades (un)',
};

export default function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState('');
  const [price, setPrice] = useState<string>('');
  const [quantity, setQuantity] = useState<string>('');
  const [unit, setUnit] = useState<UnitType>('g');

  const addItem = (e: React.FormEvent) => {
    e.preventDefault();
    if (!price || !quantity) return;

    const newItem: Item = {
      id: crypto.randomUUID(),
      name: name || `Item ${items.length + 1}`,
      price: parseFloat(price),
      quantity: parseFloat(quantity),
      unit,
    };

    setItems([...items, newItem]);
    setName('');
    setPrice('');
    setQuantity('');
  };

  const removeItem = (id: string) => {
    setItems(items.filter((item) => item.id !== id));
  };

  const clearAll = () => {
    setItems([]);
  };

  const processedItems = useMemo(() => {
    return items.map((item) => {
      let normalizedQuantity = item.quantity;
      let baseUnit = item.unit;

      // Normalize to base units for comparison
      if (item.unit === 'kg') {
        normalizedQuantity = item.quantity * 1000;
        baseUnit = 'g';
      } else if (item.unit === 'l') {
        normalizedQuantity = item.quantity * 1000;
        baseUnit = 'ml';
      }

      const pricePerUnit = item.price / normalizedQuantity;
      
      // Calculate price per standard reference (e.g., per 100g, per 1kg, per unit)
      let referencePrice = 0;
      let referenceLabel = '';

      if (baseUnit === 'g') {
        referencePrice = pricePerUnit * 1000; // Price per kg
        referenceLabel = 'por kg';
      } else if (baseUnit === 'ml') {
        referencePrice = pricePerUnit * 1000; // Price per L
        referenceLabel = 'por litro';
      } else {
        referencePrice = pricePerUnit;
        referenceLabel = 'por unidade';
      }

      return {
        ...item,
        pricePerUnit,
        referencePrice,
        referenceLabel,
      };
    });
  }, [items]);

  const bestValueId = useMemo(() => {
    if (processedItems.length < 2) return null;
    
    // Group by unit category (weight, volume, unit) to ensure fair comparison
    // For simplicity, we compare all if they are compatible (g/kg or ml/l)
    return processedItems.reduce((best, current) => {
      if (!best || current.pricePerUnit < best.pricePerUnit) {
        return current;
      }
      return best;
    }, processedItems[0])?.id;
  }, [processedItems]);

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="mb-8 text-center">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center justify-center p-3 bg-emerald-100 text-emerald-700 rounded-2xl mb-4"
          >
            <Calculator size={32} />
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-3xl font-bold text-slate-900 tracking-tight mb-2"
          >
            Comparador de Preços
          </motion.h1>
          <p className="text-slate-500 max-w-md mx-auto">
            Descubra qual produto realmente oferece o melhor custo-benefício, independente do tamanho da embalagem.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Form Section */}
          <section className="lg:col-span-4">
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200 sticky top-8">
              <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Plus size={20} className="text-emerald-600" />
                Adicionar Item
              </h2>
              
              <form onSubmit={addItem} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                    Nome (opcional)
                  </label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Ex: Arroz Marca A"
                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                      Preço (R$)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      required
                      value={price}
                      onChange={(e) => setPrice(e.target.value)}
                      placeholder="0,00"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                      Quantidade
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      required
                      value={quantity}
                      onChange={(e) => setQuantity(e.target.value)}
                      placeholder="Ex: 500"
                      className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
                    Unidade
                  </label>
                  <select
                    value={unit}
                    onChange={(e) => setUnit(e.target.value as UnitType)}
                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all bg-white"
                  >
                    {Object.entries(UNIT_LABELS).map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </div>

                <button
                  type="submit"
                  className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2 mt-2 shadow-lg shadow-emerald-200"
                >
                  <Plus size={20} />
                  Adicionar à Lista
                </button>
              </form>

              {items.length > 0 && (
                <button
                  onClick={clearAll}
                  className="w-full mt-4 text-slate-400 hover:text-red-500 text-sm font-medium transition-colors flex items-center justify-center gap-1"
                >
                  <Trash2 size={14} />
                  Limpar tudo
                </button>
              )}
            </div>
          </section>

          {/* List Section */}
          <section className="lg:col-span-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
                <ShoppingCart size={20} className="text-slate-400" />
                Itens Comparados
                <span className="bg-slate-200 text-slate-600 text-xs px-2 py-0.5 rounded-full">
                  {items.length}
                </span>
              </h2>
            </div>

            {items.length === 0 ? (
              <div className="bg-white border-2 border-dashed border-slate-200 rounded-3xl p-12 text-center">
                <div className="bg-slate-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Info size={24} className="text-slate-300" />
                </div>
                <h3 className="text-slate-600 font-medium mb-1">Nenhum item adicionado</h3>
                <p className="text-slate-400 text-sm">Adicione pelo menos dois itens para comparar qual vale mais a pena.</p>
              </div>
            ) : (
              <div className="space-y-4">
                <AnimatePresence mode="popLayout">
                  {processedItems.map((item) => {
                    const isBest = item.id === bestValueId;
                    return (
                      <motion.div
                        key={item.id}
                        layout
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className={`relative group bg-white p-5 rounded-3xl border-2 transition-all ${
                          isBest 
                            ? 'border-emerald-500 shadow-xl shadow-emerald-100' 
                            : 'border-white shadow-sm hover:border-slate-200'
                        }`}
                      >
                        {isBest && (
                          <div className="absolute -top-3 left-6 bg-emerald-500 text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full flex items-center gap-1 shadow-md">
                            <CheckCircle2 size={12} />
                            Melhor Escolha
                          </div>
                        )}

                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                          <div className="flex-1">
                            <h3 className="font-bold text-slate-900 text-lg mb-1">{item.name}</h3>
                            <div className="flex items-center gap-3 text-sm text-slate-500">
                              <span className="bg-slate-100 px-2 py-0.5 rounded-lg font-mono">
                                R$ {item.price.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                              </span>
                              <span>•</span>
                              <span>{item.quantity} {item.unit}</span>
                            </div>
                          </div>

                          <div className="flex items-center gap-6">
                            <div className="text-right">
                              <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-0.5">
                                Preço Equivalente
                              </div>
                              <div className={`text-xl font-bold ${isBest ? 'text-emerald-600' : 'text-slate-900'}`}>
                                R$ {item.referencePrice.toLocaleString('pt-BR', { minimumFractionDigits: 3 })}
                                <span className="text-xs font-normal text-slate-400 ml-1">{item.referenceLabel}</span>
                              </div>
                            </div>

                            <button
                              onClick={() => removeItem(item.id)}
                              className="p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all"
                              title="Remover item"
                            >
                              <Trash2 size={20} />
                            </button>
                          </div>
                        </div>

                        {isBest && processedItems.length > 1 && (
                          <div className="mt-4 pt-4 border-t border-emerald-50 flex items-center gap-2 text-xs text-emerald-600 font-medium">
                            <AlertCircle size={14} />
                            Este item custa menos por unidade de medida.
                          </div>
                        )}
                      </motion.div>
                    );
                  })}
                </AnimatePresence>
              </div>
            )}

            {items.length > 0 && (
              <div className="mt-8 p-6 bg-slate-900 rounded-3xl text-white overflow-hidden relative">
                <div className="relative z-10">
                  <h3 className="text-lg font-semibold mb-2 flex items-center gap-2">
                    <Info size={20} className="text-emerald-400" />
                    Dica de Economia
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    Muitas vezes, embalagens maiores parecem mais baratas, mas o preço por quilo ou litro pode ser maior. 
                    Sempre compare o valor unitário para garantir que você está levando a melhor oferta para casa.
                  </p>
                </div>
                <div className="absolute -right-8 -bottom-8 opacity-10">
                  <ShoppingCart size={160} />
                </div>
              </div>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
