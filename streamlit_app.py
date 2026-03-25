import streamlit as st
import streamlit.components.v1 as components

# 1. Configuração da página do Streamlit (Ícone da Aba do Navegador)
st.set_page_config(
    page_title="Comparador de Preços Inteligente",
    page_icon="https://i.imgur.com/NVmQbJT.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Truque para o ícone da tela inicial (iOS e Android)
st.markdown("""
    <head>
        <link rel="apple-touch-icon" href="https://i.imgur.com/NVmQbJT.png">
        <link rel="icon" href="https://i.imgur.com/NVmQbJT.png">
    </head>
""", unsafe_allow_html=True)

# 3. Estilos customizados para o Streamlit para esconder menus e padding desnecessário
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# 4. O código HTML/React completo (Interface Visual)
html_code = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparador de Preços</title>
    <link rel="icon" type="image/png" href="https://i.imgur.com/NVmQbJT.png">
    <link rel="apple-touch-icon" href="https://i.imgur.com/NVmQbJT.png">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- React & ReactDOM -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <!-- Babel para JSX -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
            margin: 0;
            padding: 0;
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useMemo, useEffect } = React;

        // Ícones Lucide (Helper para renderizar via SVG)
        const Icon = ({ name, size = 20, className = "" }) => {
            useEffect(() => {
                lucide.createIcons();
            }, []);
            return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
        };

        const UNIT_LABELS = {
            g: 'Gramas (g)',
            kg: 'Quilos (kg)',
            ml: 'Mililitros (ml)',
            l: 'Litros (l)',
            un: 'Unidades (un)',
        };

        function App() {
            const [items, setItems] = useState([]);
            const [name, setName] = useState('');
            const [price, setPrice] = useState('');
            const [quantity, setQuantity] = useState('');
            const [unit, setUnit] = useState('g');

            const addItem = (e) => {
                e.preventDefault();
                if (!price || !quantity) return;

                const newItem = {
                    id: Math.random().toString(36).substr(2, 9),
                    name: name || `Item ${items.length + 1}`,
                    price: parseFloat(price),
                    quantity: parseFloat(quantity),
                    unit,
                };

                setItems([...items, newItem]);
                setName('');
                setPrice('');
                setQuantity('');
                
                // Re-inicializa os ícones após renderizar novos elementos
                setTimeout(() => lucide.createIcons(), 0);
            };

            const removeItem = (id) => {
                setItems(items.filter((item) => item.id !== id));
            };

            const clearAll = () => {
                setItems([]);
            };

            const processedItems = useMemo(() => {
                return items.map((item) => {
                    let normalizedQuantity = item.quantity;
                    let baseUnit = item.unit;

                    if (item.unit === 'kg') {
                        normalizedQuantity = item.quantity * 1000;
                        baseUnit = 'g';
                    } else if (item.unit === 'l') {
                        normalizedQuantity = item.quantity * 1000;
                        baseUnit = 'ml';
                    }

                    const pricePerUnit = item.price / normalizedQuantity;
                    let referencePrice = 0;
                    let referenceLabel = '';

                    if (baseUnit === 'g') {
                        referencePrice = pricePerUnit * 1000;
                        referenceLabel = 'por kg';
                    } else if (baseUnit === 'ml') {
                        referencePrice = pricePerUnit * 1000;
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
                return processedItems.reduce((best, current) => {
                    if (!best || current.pricePerUnit < best.pricePerUnit) {
                        return current;
                    }
                    return best;
                }, processedItems[0])?.id;
            }, [processedItems]);

            useEffect(() => {
                lucide.createIcons();
            }, [items]);

            return (
                <div className="min-h-screen bg-slate-50 p-4 md:p-8">
                    <div className="max-w-4xl mx-auto">
                        {/* Header */}
                        <header className="mb-8 text-center">
                            <div className="inline-flex items-center justify-center p-3 bg-emerald-100 text-emerald-700 rounded-2xl mb-4">
                                <Icon name="calculator" size={32} />
                            </div>
                            <h1 className="text-3xl font-bold text-slate-900 tracking-tight mb-2">
                                Comparador de Preços
                            </h1>
                            <p className="text-slate-500 max-w-md mx-auto">
                                Descubra qual produto realmente oferece o melhor custo-benefício, independente do tamanho da embalagem.
                            </p>
                        </header>

                        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                            {/* Form Section */}
                            <section className="lg:col-span-4">
                                <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200 sticky top-8">
                                    <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
                                        <Icon name="plus" size={20} className="text-emerald-600" />
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
                                                onChange={(e) => setUnit(e.target.value)}
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
                                            <Icon name="plus" size={20} />
                                            Adicionar à Lista
                                        </button>
                                    </form>

                                    {items.length > 0 && (
                                        <button
                                            onClick={clearAll}
                                            className="w-full mt-4 text-slate-400 hover:text-red-500 text-sm font-medium transition-colors flex items-center justify-center gap-1"
                                        >
                                            <Icon name="trash-2" size={14} />
                                            Limpar tudo
                                        </button>
                                    )}
                                </div>
                            </section>

                            {/* List Section */}
                            <section className="lg:col-span-8">
                                <div className="flex items-center justify-between mb-4">
                                    <h2 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
                                        <Icon name="shopping-cart" size={20} className="text-slate-400" />
                                        Itens Comparados
                                        <span className="bg-slate-200 text-slate-600 text-xs px-2 py-0.5 rounded-full">
                                            {items.length}
                                        </span>
                                    </h2>
                                </div>

                                {items.length === 0 ? (
                                    <div className="bg-white border-2 border-dashed border-slate-200 rounded-3xl p-12 text-center">
                                        <div className="bg-slate-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                            <Icon name="info" size={24} className="text-slate-300" />
                                        </div>
                                        <h3 className="text-slate-600 font-medium mb-1">Nenhum item adicionado</h3>
                                        <p className="text-slate-400 text-sm">Adicione pelo menos dois itens para comparar qual vale mais a pena.</p>
                                    </div>
                                ) : (
                                    <div className="space-y-4">
                                        {processedItems.map((item) => {
                                            const isBest = item.id === bestValueId;
                                            return (
                                                <div
                                                    key={item.id}
                                                    className={`relative bg-white p-5 rounded-3xl border-2 transition-all ${
                                                        isBest 
                                                            ? 'border-emerald-500 shadow-xl shadow-emerald-100' 
                                                            : 'border-white shadow-sm hover:border-slate-200'
                                                    }`}
                                                >
                                                    {isBest && (
                                                        <div className="absolute -top-3 left-6 bg-emerald-500 text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full flex items-center gap-1 shadow-md">
                                                            <Icon name="check-circle-2" size={12} />
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
                                                                <Icon name="trash-2" size={20} />
                                                            </button>
                                                        </div>
                                                    </div>

                                                    {isBest && p
